from deltacat import TableReadOptimizationLevel, SchemaEvolutionMode, SchemaConsistencyType
from deltacat.types.tables import TablePropertyDefaultValues, TableProperty

DEFAULT_TABLE_PROPERTIES = TablePropertyDefaultValues


class TableProperties(dict):
    @staticmethod
    def of(
        read_optimization_level: TableReadOptimizationLevel,
        default_compaction_hash_bucket_count: int,
        records_per_compacted_file: int,
        appended_record_count_compaction_trigger: int,
        appended_file_count_compaction_trigger: int,
        appended_delta_count_compaction_trigger: int,
        schema_evolution_mode: SchemaEvolutionMode,
        default_schema_consistency_type: SchemaConsistencyType,
    ) -> 'TableProperties':
        table_properties = TableProperties()
        table_properties.read_optimization_level = read_optimization_level
        table_properties.default_compaction_hash_bucket_count = default_compaction_hash_bucket_count
        table_properties.records_per_compacted_file = records_per_compacted_file
        table_properties.appended_record_count_compaction_trigger = appended_record_count_compaction_trigger
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
    def default_compaction_hash_bucket_count(self, value) -> None:
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
        # Set the value as in TablePropertyDefaultValues in deltacat
        multiplied_value = value * self.default_compaction_hash_bucket_count * 2
        if multiplied_value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.APPENDED_RECORD_COUNT_COMPACTION_TRIGGER):
          self['appended_record_count_compaction_trigger'] = multiplied_value

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
    def default_schema_consistency_type(self, value: SchemaConsistencyType):
        if value != DEFAULT_TABLE_PROPERTIES.get(TableProperty.DEFAULT_SCHEMA_CONSISTENCY_TYPE):
          self['default_schema_consistency_type'] = value