import os

def model(dbt, session):
    # incrementalマテリアライゼーション、タグ、ユニークキーの設定
    dbt.config(
        materialized="incremental",
        tags=["python", "dml_sample"],
        unique_key="id"
    )
    
    # ターゲットテーブルの完全名称をdbt.thisで取得
    target_table = dbt.this

    # 外部ファイル "sql_statements.sql" のパスを取得（このモデルと同じディレクトリに配置）
    file_path = os.path.join(os.path.dirname(__file__), "sql_statements.sql")
    
    # 外部SQLファイルを読み込む
    with open(file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    
    # 外部ファイル内のプレースホルダー {target_table} をターゲットテーブル名に置換
    sql_content = sql_content.format(target_table=target_table)
    
    # セミコロンで区切り、各SQL文のリストを作成（空文は除外）
    sql_statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
    
    # 各SQL文を順次実行
    for stmt in sql_statements:
        session.sql(stmt).collect()
    
    # 最終的なターゲットテーブルの内容を返す
    return session.table(target_table)
