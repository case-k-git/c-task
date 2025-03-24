import os
from jinja2 import Environment, FileSystemLoader

def model(dbt, session):
    dbt.config(
        materialized="incremental",
        tags=["python", "dml_sample"],
        unique_key="id"
    )
    target_table = dbt.this
    # 外部から渡す source_table は、例えば dbt の設定（vars や config）経由で渡すことを想定
    source_table = dbt.config.get("source_table")
    if not source_table:
        raise ValueError("source_table must be provided in the configuration")

    # 現在のスクリプトのディレクトリをテンプレートのルートディレクトリとして設定
    template_dir = os.path.dirname(__file__)
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # sql_statements.sql をテンプレートとして読み込む
    template = env.get_template("sql_statements.sql")
    rendered_sql = template.render(target_table=target_table, source_table=source_table)
    
    # セミコロンで区切られたSQL文を個別に実行
    sql_statements = [stmt.strip() for stmt in rendered_sql.split(";") if stmt.strip()]
    for stmt in sql_statements:
        session.sql(stmt).collect()
    
    return session.table(target_table)
