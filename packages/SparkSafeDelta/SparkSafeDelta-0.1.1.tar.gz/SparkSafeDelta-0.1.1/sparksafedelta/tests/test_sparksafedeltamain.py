def delta_write_safe(sp_df_to_write):
    missing_columns = get_missing_columns(sp_df_to_write)
    if missing_columns:
        implement_missing_columns(missing_columns)
    sp_df_to_write.write.insertInto(DATABRICKS_TABLE_NAME)
    
def get_missing_columns(sp_df_to_insert):
    existing_table = spark.sql("SELECT * FROM " + DATABRICKS_TABLE_NAME)
    existing_columns = set(existing_table.columns)
    new_columns = set(sp_df_to_insert.columns)
    returnable = list(set.difference(new_columns, existing_columns))
    if len(returnable) == 0:
        return False
    else:
        return returnable
      
def implement_missing_columns(missing_column_list):
    for column in missing_column_list:
        spark.sql("ALTER TABLE " + DATABRICKS_TABLE_NAME + " ADD COLUMNS (" + column + " STRING)")      