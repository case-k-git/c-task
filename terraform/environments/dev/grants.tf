# Databricksのグラントリソースモジュール
resource "databricks_grants" "workspace_grants" {
  for_each = local.inputs.workspace_grants
  workspace = true
  
  dynamic "grants" {
    for_each = each.value.grants
    content {
      principal  = grants.value.principal
      privileges = grants.value.privileges
    }
  }
}

resource "databricks_grants" "catalog_grants" {
  for_each = local.inputs.catalog_grants
  catalog = each.value.catalog_name != null ? each.value.catalog_name : local.project_name

  dynamic "grants" {
    for_each = each.value.grants
    content {
      principal  = grants.value.principal
      privileges = grants.value.privileges
    }
  }
}

# スキーマレベルの権限設定
resource "databricks_grants" "schema_grants" {
  for_each = local.inputs.schema_grants
  
  schema {
    catalog_name = each.value.catalog_name != null ? each.value.catalog_name : local.project_name
    schema_name  = each.value.schema_name != null ? each.value.schema_name : "${local.environment}_schema"
  }

  dynamic "grants" {
    for_each = each.value.grants
    content {
      principal  = grants.value.principal
      privileges = grants.value.privileges
    }
  }
}

# テーブルレベルの権限設定
resource "databricks_grants" "table_grants" {
  for_each = local.inputs.tables
  
  table {
    catalog_name = each.value.catalog_name != null ? each.value.catalog_name : local.project_name
    schema_name  = each.value.schema_name != null ? each.value.schema_name : "${local.environment}_schema"
    table_name   = each.value.table_name
  }

  dynamic "grants" {
    for_each = local.inputs.table_grants[each.key]
    content {
      principal  = grants.value.principal
      privileges = grants.value.privileges
    }
  }
}
