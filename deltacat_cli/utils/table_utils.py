from typing import ClassVar

import pyarrow as pa
from deltacat.types.tables import TableProperty, TablePropertyDefaultValues

from deltacat import Field, SchemaConsistencyType, SchemaEvolutionMode, TableReadOptimizationLevel
from deltacat import Schema as DeltacatSchema


DEFAULT_TABLE_PROPERTIES = TablePropertyDefaultValues


class TableProperties(dict):
    @staticmethod
    def of(
        read_optimization_level: TableReadOptimizationLevel,
        default_compaction_hash_bucket_count: int,
        records_per_compacted_file: int,
        appended_file_count_compaction_trigger: int,
        appended_delta_count_compaction_trigger: int,
        schema_evolution_mode: SchemaEvolutionMode,
        default_schema_consistency_type: SchemaConsistencyType,
    ) -> 'TableProperties':
        table_properties = TableProperties()
        table_properties.read_optimization_level = read_optimization_level
        table_properties.default_compaction_hash_bucket_count = default_compaction_hash_bucket_count
        table_properties.records_per_compacted_file = records_per_compacted_file
        # Set the appended_record_count_compaction_trigger as in TablePropertyDefaultValues in deltacat
        table_properties.appended_record_count_compaction_trigger = (
            records_per_compacted_file * default_compaction_hash_bucket_count * 2
        )
        table_properties.appended_file_count_compaction_trigger = appended_file_count_compaction_trigger
        table_properties.appended_delta_count_compaction_trigger = appended_delta_count_compaction_trigger
        table_properties.schema_evolution_mode = schema_evolution_mode
        table_properties.default_schema_consistency_type = default_schema_consistency_type
        return table_properties

    @property
    def read_optimization_level(self) -> TableReadOptimizationLevel | None:
        return self.get('read_optimization_level')

    @read_optimization_level.setter
    def read_optimization_level(self, value: TableReadOptimizationLevel) -> None:
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.READ_OPTIMIZATION_LEVEL):
            self['read_optimization_level'] = value

    @property
    def default_compaction_hash_bucket_count(self) -> int | None:
        return self.get('default_compaction_hash_bucket_count')

    @default_compaction_hash_bucket_count.setter
    def default_compaction_hash_bucket_count(self, value: int) -> None:
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.DEFAULT_COMPACTION_HASH_BUCKET_COUNT):
            self['default_compaction_hash_bucket_count'] = value

    @property
    def records_per_compacted_file(self) -> int | None:
        return self.get('records_per_compacted_file')

    @records_per_compacted_file.setter
    def records_per_compacted_file(self, value: int) -> None:
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.RECORDS_PER_COMPACTED_FILE):
            self['records_per_compacted_file'] = value

    @property
    def appended_record_count_compaction_trigger(self) -> int | None:
        return self.get('appended_record_count_compaction_trigger')

    @appended_record_count_compaction_trigger.setter
    def appended_record_count_compaction_trigger(self, value: int) -> None:
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.APPENDED_RECORD_COUNT_COMPACTION_TRIGGER):
            self['appended_record_count_compaction_trigger'] = value

    @property
    def appended_file_count_compaction_trigger(self) -> int | None:
        return self.get('appended_file_count_compaction_trigger')

    @appended_file_count_compaction_trigger.setter
    def appended_file_count_compaction_trigger(self, value: int) -> None:
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.APPENDED_FILE_COUNT_COMPACTION_TRIGGER):
            self['appended_file_count_compaction_trigger'] = value

    @property
    def appended_delta_count_compaction_trigger(self) -> int | None:
        return self.get('appended_delta_count_compaction_trigger')

    @appended_delta_count_compaction_trigger.setter
    def appended_delta_count_compaction_trigger(self, value: int) -> None:
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.APPENDED_DELTA_COUNT_COMPACTION_TRIGGER):
            self['appended_delta_count_compaction_trigger'] = value

    @property
    def schema_evolution_mode(self) -> SchemaEvolutionMode:
        return self.get('schema_evolution_mode')

    @schema_evolution_mode.setter
    def schema_evolution_mode(self, value: SchemaEvolutionMode) -> None:
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.SCHEMA_EVOLUTION_MODE):
            self['schema_evolution_mode'] = value

    @property
    def default_schema_consistency_type(self) -> SchemaConsistencyType | None:
        return self.get('default_schema_consistency_type')

    @default_schema_consistency_type.setter
    def default_schema_consistency_type(self, value: SchemaConsistencyType) -> None:
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.DEFAULT_SCHEMA_CONSISTENCY_TYPE):
            self['default_schema_consistency_type'] = value


class TableSchema:
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

    def __init__(self):
        self._merge_keys = None
        self._deltacat_schema = None

    @staticmethod
    def of(schema: str, merge_keys: str) -> 'TableSchema':
        table_schema = TableSchema()
        table_schema.merge_keys = merge_keys
        table_schema.deltacat_schema = schema
        return table_schema

    @property
    def type_mapping(self) -> dict[str, pa.DataType]:
        """Mapping for pyarrow types."""
        return self.TYPE_MAPPING

    @property
    def merge_keys(self) -> list[str]:
        return self._merge_keys

    @merge_keys.setter
    def merge_keys(self, merge_keys: str) -> None:
        self._merge_keys = [key.strip() for key in merge_keys.split(',') if key.strip()] if merge_keys else None

    @property
    def deltacat_table_schema(self) -> DeltacatSchema:
        return self._deltacat_schema

    @deltacat_table_schema.setter
    def deltacat_table_schema(self, schema: str) -> None:
        schema = self._parse_schema(schema)
        arrow_schema = self._get_arrow_schema(schema)
        self._deltacat_schema = self._get_deltacat_schema(arrow_schema)

    def _parse_schema(self, schema: str) -> dict[str, str] | None:
        return (
            {pair.split(':', 1)[0].strip(): pair.split(':', 1)[1].strip() for pair in schema.split(',') if ':' in pair}
            if schema
            else None
        )

    def _get_deltacat_schema(self, arrow_schema: pa.Schema) -> DeltacatSchema:
        fields = []
        for field in arrow_schema:
            field: pa.Field
            if field.name in self.merge_keys:
                fields.append(Field.of(field, is_merge_key=True))
            else:
                fields.append(Field.of(field))

        return DeltacatSchema.of(fields)

    def _get_arrow_schema(self, schema: dict[str, str]) -> pa.Schema:
        fields = []

        for field_name, field_type in schema.items():
            arrow_type = self.type_mapping.get(field_type)
            if not arrow_type:
                arrow_type = self.type_mapping.get('string')
            arrow_field = pa.field(name=field_name, type=arrow_type)
            fields.append(arrow_field)

        return pa.schema(fields)
