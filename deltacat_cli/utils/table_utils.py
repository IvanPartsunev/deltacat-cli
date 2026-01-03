import pyarrow as pa

from deltacat import Field, SchemaConsistencyType, SchemaEvolutionMode, TableReadOptimizationLevel
from deltacat import Schema as DeltacatSchema


TYPE_MAPPING: dict[str, pa.DataType] = {
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


class TableProperties(dict):
    @staticmethod
    def of(
        read_optimization_level: TableReadOptimizationLevel | None = None,
        default_compaction_hash_bucket_count: int | None = None,
        records_per_compacted_file: int | None = None,
        appended_file_count_compaction_trigger: int | None = None,
        appended_delta_count_compaction_trigger: int | None = None,
        schema_evolution_mode: SchemaEvolutionMode | None = None,
        default_schema_consistency_type: SchemaConsistencyType | None = None,
    ) -> 'TableProperties':
        table_properties = TableProperties()
        table_properties.read_optimization_level = read_optimization_level
        table_properties.default_compaction_hash_bucket_count = default_compaction_hash_bucket_count
        table_properties.records_per_compacted_file = records_per_compacted_file
        # Set the appended_record_count_compaction_trigger as in TablePropertyDefaultValues in deltacat
        # Only calculate if both values are not None
        if records_per_compacted_file is not None and default_compaction_hash_bucket_count is not None:
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
    def read_optimization_level(self, value: TableReadOptimizationLevel | None) -> None:
        if value:
            self['read_optimization_level'] = value

    @property
    def default_compaction_hash_bucket_count(self) -> int | None:
        return self.get('default_compaction_hash_bucket_count')

    @default_compaction_hash_bucket_count.setter
    def default_compaction_hash_bucket_count(self, value: str | None) -> None:
        if value:
            self['default_compaction_hash_bucket_count'] = value

    @property
    def records_per_compacted_file(self) -> int | None:
        return self.get('records_per_compacted_file')

    @records_per_compacted_file.setter
    def records_per_compacted_file(self, value: int | None) -> None:
        if value:
            self['records_per_compacted_file'] = value

    @property
    def appended_record_count_compaction_trigger(self) -> int | None:
        return self.get('appended_record_count_compaction_trigger')

    @appended_record_count_compaction_trigger.setter
    def appended_record_count_compaction_trigger(self, value: int | None) -> None:
        if value:
            self['appended_record_count_compaction_trigger'] = value

    @property
    def appended_file_count_compaction_trigger(self) -> int | None:
        return self.get('appended_file_count_compaction_trigger')

    @appended_file_count_compaction_trigger.setter
    def appended_file_count_compaction_trigger(self, value: int | None) -> None:
        if value:
            self['appended_file_count_compaction_trigger'] = value

    @property
    def appended_delta_count_compaction_trigger(self) -> int | None:
        return self.get('appended_delta_count_compaction_trigger')

    @appended_delta_count_compaction_trigger.setter
    def appended_delta_count_compaction_trigger(self, value: int | None) -> None:
        if value:
            self['appended_delta_count_compaction_trigger'] = value

    @property
    def schema_evolution_mode(self) -> SchemaEvolutionMode:
        return self.get('schema_evolution_mode')

    @schema_evolution_mode.setter
    def schema_evolution_mode(self, value: SchemaEvolutionMode | None) -> None:
        if value:
            self['schema_evolution_mode'] = value

    @property
    def default_schema_consistency_type(self) -> SchemaConsistencyType | None:
        return self.get('default_schema_consistency_type')

    @default_schema_consistency_type.setter
    def default_schema_consistency_type(self, value: SchemaConsistencyType | None) -> None:
        if value:
            self['default_schema_consistency_type'] = value


class TableSchema(dict):
    @staticmethod
    def of(schema: str | None) -> 'TableSchema':
        if schema:
            return TableSchema(
                {pair.split(':', 1)[0].strip(): pair.split(':', 1)[1].strip() for pair in schema.split(',') if ':' in pair}
            )
        return TableSchema()


class DeltacatTableSchema:
    @staticmethod
    def of(schema: TableSchema, merge_keys: str) -> 'DeltacatSchema':
        """Build Deltacat Schema."""

        arrow_fields = []
        for field_name, field_type in schema.items():
            arrow_type = TYPE_MAPPING.get(field_type)
            if not arrow_type:
                arrow_type = TYPE_MAPPING.get('string')
            arrow_field = pa.field(name=field_name, type=arrow_type)
            arrow_fields.append(arrow_field)

        arrow_schema = pa.schema(arrow_fields)

        merge_keys = [key.strip() for key in merge_keys.split(',') if key.strip()] if merge_keys else None

        dc_fields = []
        for field in arrow_schema:
            field: pa.Field
            if field.name in merge_keys:
                dc_fields.append(Field.of(field, is_merge_key=True))
            else:
                dc_fields.append(Field.of(field))

        return DeltacatSchema.of(dc_fields)
