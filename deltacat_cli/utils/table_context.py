from typing import ClassVar

import pyarrow as pa

from deltacat import (
    Field,
    LifecycleState,
    Schema,
    TableDefinition,
    TableProperty,
    TableReadOptimizationLevel,
    SchemaEvolutionMode,
    SchemaConsistencyType,
)
from deltacat import create_table as dc_create_table
from deltacat.compute.compactor_v2.constants import MAX_RECORDS_PER_COMPACTED_FILE


class TableContext:
    """Table context setting up table operations."""

    TYPE_MAPPING: ClassVar[dict[str, pa.DataType]] = {
        'int64': pa.int64(),
        'int32': pa.int32(),
        'float64': pa.float64(),
        'float32': pa.float32(),
        'string': pa.large_string(),
        'bool': pa.bool_(),
        'date': pa.date32(),
        'timestamp[s]': pa.timestamp('s', 'UTC'),
        'timestamp[ms]': pa.timestamp('ms', 'UTC'),
        'timestamp[us]': pa.timestamp('us', 'UTC'),
        'timestamp[ns]': pa.timestamp('ns', 'UTC'),
        'time[s]': pa.time32('s'),
        'time[ms]': pa.time32('ms'),
        'time[us]': pa.time64('us'),
        'time[ns]': pa.time64('ns'),
    }

    @property
    def type_mapping(self) -> dict[str, pa.DataType]:
        """Mapping for pyarrow types."""
        return self.TYPE_MAPPING

    def create_table(
        self,
        name: str,
        namespace: str,
        catalog_name: str,
        merge_keys: list[str] | None = None,
        table_version: str | None = None,
        lifecycle_state: LifecycleState | None = LifecycleState.ACTIVE,
        schema: dict[str, str] | None = None,
        table_description: str | None = None,
        table_version_description: str | None = None,
        compaction: bool = True,
    ) -> TableDefinition:
        """Create a DeltaCAT table with given arguments.
        This method implements only part of possible arguments available in DeltaCat API.
        """

        schema_ = self._set_deltacat_table_schema(schema, merge_keys or []) if schema else None

        table_properties = (
            {TableProperty.READ_OPTIMIZATION_LEVEL: TableReadOptimizationLevel.NONE} if not compaction else None
        )

        return dc_create_table(
            table=name,
            namespace=namespace,
            catalog=catalog_name,
            table_version=table_version,
            schema=schema_,
            table_description=table_description,
            table_version_description=table_version_description,
            lifecycle_state=lifecycle_state,
            fail_if_exists=True,
            auto_create_namespace=True,
            table_properties=table_properties,
        )

    def _set_deltacat_table_schema(self, schema: dict[str, str], merge_keys: list[str]) -> Schema:
        arrow_schema = self._shema_to_arrow(schema)

        fields = []
        for field in arrow_schema:
            field: pa.Field
            if field.name in merge_keys:
                fields.append(Field.of(field, is_merge_key=True))
            else:
                fields.append(Field.of(field))

        return Schema.of(fields)

    def _shema_to_arrow(self, schema: dict[str, str]) -> pa.Schema:
        fields = []

        for field_name, field_type in schema.items():
            arrow_type = self.type_mapping.get(field_type)
            if not arrow_type:
                arrow_type = self.type_mapping.get('string')
            arrow_field = pa.field(name=field_name, type=arrow_type)
            fields.append(arrow_field)

        return pa.schema(fields)

    def set_table_properties(
        self,
        read_optimization_level: TableReadOptimizationLevel,
        records_per_compacted_file: int,
        appended_record_count_compaction_trigger: int,
        appended_file_count_compaction_trigger: int,
        appended_delta_count_compaction_trigger: int,
        default_compaction_hash_bucket_count: int,
        schema_evolution_mode: SchemaEvolutionMode,
        default_schema_consistency_type: SchemaConsistencyType,
    ):
        TablePropertyDefaultValues = {
            TableProperty.READ_OPTIMIZATION_LEVEL: TableReadOptimizationLevel.MAX,
            TableProperty.RECORDS_PER_COMPACTED_FILE: MAX_RECORDS_PER_COMPACTED_FILE,
            TableProperty.APPENDED_RECORD_COUNT_COMPACTION_TRIGGER: MAX_RECORDS_PER_COMPACTED_FILE
            * 16,  # DEFAULT_COMPACTION_HASH_BUCKET_COUNT * 2
            TableProperty.APPENDED_FILE_COUNT_COMPACTION_TRIGGER: 1000,
            TableProperty.APPENDED_DELTA_COUNT_COMPACTION_TRIGGER: 100,
            TableProperty.DEFAULT_COMPACTION_HASH_BUCKET_COUNT: 8,
            TableProperty.SCHEMA_EVOLUTION_MODE: SchemaEvolutionMode.AUTO,
            TableProperty.DEFAULT_SCHEMA_CONSISTENCY_TYPE: SchemaConsistencyType.NONE,
        }


table_context = TableContext()
