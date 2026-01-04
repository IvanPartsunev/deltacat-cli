"""Unit tests for deltacat CLI table operations."""

import shutil
import tempfile
from collections.abc import Generator
from typing import Any
from unittest.mock import Mock, patch

import deltacat.catalog.main.impl as catalog
import pyarrow as pa
import pytest
from deltacat.catalog import get_catalog_properties
from deltacat.exceptions import TableAlreadyExistsError, TableNotFoundError
from typer.testing import CliRunner

from deltacat import LifecycleState, SchemaEvolutionMode, TableReadOptimizationLevel
from deltacat_cli.main import app
from deltacat_cli.utils.table_utils import DeltacatTableSchema, TableProperties, TableSchema


@pytest.fixture(scope='class')
def catalog_setup() -> Generator[tuple[str, Any], None, None]:
    """Setup and teardown for the catalog test environment."""
    temp_dir = tempfile.mkdtemp()
    catalog_properties = get_catalog_properties(root=temp_dir)
    yield temp_dir, catalog_properties

    # Teardown
    shutil.rmtree(temp_dir)


@pytest.fixture(scope='function')
def test_namespace(catalog_setup: tuple[str, Any]) -> tuple[str, Any]:
    """Create a test namespace for each test."""
    _, catalog_properties = catalog_setup
    namespace_name = 'test_table_cli_namespace'

    if not catalog.namespace_exists(namespace_name, inner=catalog_properties):
        catalog.create_namespace(
            namespace=namespace_name, properties={'description': 'Test Table CLI Namespace'}, inner=catalog_properties
        )

    return namespace_name, catalog_properties


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_arrow_schema() -> pa.Schema:
    """Create a sample PyArrow schema for testing."""
    return pa.schema([pa.field('id', pa.int64()), pa.field('name', pa.string()), pa.field('value', pa.float64())])


class TestTableCreateCLI:
    """Test the table create CLI command."""

    def test_create_table_basic(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test basic table creation via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.create_table') as mock_create_table,
        ):
            # Setup mocks
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_table.table.table_name = 'test_table'
            mock_table.table_version.namespace = namespace_name
            mock_create_table.return_value = mock_table

            result = runner.invoke(
                app,
                [
                    'table',
                    'create',
                    '--name',
                    'test_table',
                    '--namespace',
                    namespace_name,
                    '--table-description',
                    'Test table description',
                ],
            )

            assert result.exit_code == 0
            mock_create_table.assert_called_once()
            call_args = mock_create_table.call_args
            assert call_args.kwargs['table'] == 'test_table'
            assert call_args.kwargs['namespace'] == namespace_name
            assert call_args.kwargs['catalog'] == 'test_catalog'
            assert call_args.kwargs['fail_if_exists'] is True
            assert call_args.kwargs['auto_create_namespace'] is True

    def test_create_table_with_schema(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test table creation with schema via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.create_table') as mock_create_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_create_table.return_value = mock_table

            result = runner.invoke(
                app,
                [
                    'table',
                    'create',
                    '--name',
                    'test_table_schema',
                    '--namespace',
                    namespace_name,
                    '--schema',
                    'id:int64,name:string,created_at:timestamp[s]',
                    '--merge-keys',
                    'id',
                ],
            )

            assert result.exit_code == 0
            mock_create_table.assert_called_once()
            call_args = mock_create_table.call_args
            assert call_args.kwargs['schema'] is not None

    def test_create_table_with_properties(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test table creation with table properties via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.create_table') as mock_create_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_create_table.return_value = mock_table

            result = runner.invoke(
                app,
                [
                    'table',
                    'create',
                    '--name',
                    'test_table_props',
                    '--namespace',
                    namespace_name,
                    '--read-optimization-level',
                    'MAX',
                    '--default-compaction-hash-bucket-count',
                    '16',
                    '--records-per-compacted-file',
                    '5000000',
                    '--appended-file-count-compaction-trigger',
                    '500',
                    '--appended-delta-count-compaction-trigger',
                    '50',
                    '--schema-evolution-mode',
                    'AUTO',
                    '--default-schema-consistency-type',
                    'NONE',
                ],
            )

            assert result.exit_code == 0
            mock_create_table.assert_called_once()
            call_args = mock_create_table.call_args

            # Verify table properties were passed
            table_properties = call_args.kwargs.get('table_properties')
            assert table_properties is not None

    def test_create_table_with_version(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test table creation with specific version via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.create_table') as mock_create_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_create_table.return_value = mock_table

            result = runner.invoke(
                app,
                [
                    'table',
                    'create',
                    '--name',
                    'test_table_version',
                    '--namespace',
                    namespace_name,
                    '--table-version',
                    'v1.0.0',
                    '--table-version-description',
                    'Initial version',
                ],
            )

            assert result.exit_code == 0
            mock_create_table.assert_called_once()
            call_args = mock_create_table.call_args
            assert 'table_version' in call_args.kwargs
            assert call_args.kwargs['table_version'] == 'v1.0.0'
            assert 'table_version_description' in call_args.kwargs
            assert call_args.kwargs['table_version_description'] == 'Initial version'

    def test_create_table_without_optional_params(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test that None values are not passed to create_table function."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.create_table') as mock_create_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_create_table.return_value = mock_table

            result = runner.invoke(
                app, ['table', 'create', '--name', 'test_table_minimal', '--namespace', namespace_name]
            )

            assert result.exit_code == 0
            mock_create_table.assert_called_once()
            call_args = mock_create_table.call_args

            # Verify None values are not passed
            assert 'table_version' not in call_args.kwargs
            assert 'table_description' not in call_args.kwargs
            assert 'table_version_description' not in call_args.kwargs
            assert 'lifecycle_state' not in call_args.kwargs
            assert 'table_properties' not in call_args.kwargs

    def test_create_table_show_types_help(self, runner: CliRunner) -> None:
        """Test the --show-types-help flag."""
        result = runner.invoke(app, ['table', 'create', '--show-types-help'])

        assert result.exit_code == 0
        assert 'Available Data Types:' in result.output
        assert 'int64' in result.output
        assert 'string' in result.output
        assert 'timestamp[s]' in result.output

    def test_create_table_error_handling(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test error handling in table creation."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.create_table') as mock_create_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_create_table.side_effect = TableAlreadyExistsError('Table already exists')

            result = runner.invoke(app, ['table', 'create', '--name', 'existing_table', '--namespace', namespace_name])

            assert result.exit_code == 1
            assert 'Table already exists' in result.output


class TestTableAlterCLI:
    """Test the table alter CLI command."""

    def test_alter_table_description(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test altering table description via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.catalog.main.impl.get_table') as mock_get_table,
            patch('deltacat.alter_table') as mock_alter_table,
            patch('deltacat.refresh_table') as mock_refresh_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_table.table_version.name = 'test_table'
            mock_table.table_version.schema = Mock()
            mock_get_table.return_value = mock_table

            result = runner.invoke(
                app,
                [
                    'table',
                    'alter',
                    '--name',
                    'test_table',
                    '--namespace',
                    namespace_name,
                    '--table-description',
                    'Updated description',
                ],
            )

            assert result.exit_code == 0
            mock_alter_table.assert_called_once()
            call_args = mock_alter_table.call_args
            assert call_args.kwargs['table'] == 'test_table'
            assert call_args.kwargs['namespace'] == namespace_name
            assert call_args.kwargs['table_description'] == 'Updated description'
            mock_refresh_table.assert_called_once_with('test_table')

    def test_alter_table_lifecycle_state(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test altering table lifecycle state via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.catalog.main.impl.get_table') as mock_get_table,
            patch('deltacat.alter_table') as mock_alter_table,
            patch('deltacat.refresh_table') as mock_refresh_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_table.table_version.name = 'test_table'
            mock_table.table_version.schema = Mock()
            mock_get_table.return_value = mock_table

            result = runner.invoke(
                app,
                [
                    'table',
                    'alter',
                    '--name',
                    'test_table',
                    '--namespace',
                    namespace_name,
                    '--lifecycle-state',
                    'DEPRECATED',
                ],
            )

            assert result.exit_code == 0
            mock_alter_table.assert_called_once()
            call_args = mock_alter_table.call_args
            assert call_args.kwargs['lifecycle_state'] == LifecycleState.DEPRECATED

    def test_alter_table_schema_updates(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test altering table schema via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.catalog.main.impl.get_table') as mock_get_table,
            patch('deltacat.alter_table') as mock_alter_table,
            patch('deltacat.refresh_table') as mock_refresh_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_table.table_version.name = 'test_table'
            mock_table.table_version.schema = Mock()
            mock_get_table.return_value = mock_table

            result = runner.invoke(
                app,
                [
                    'table',
                    'alter',
                    '--name',
                    'test_table',
                    '--namespace',
                    namespace_name,
                    '--schema-updates',
                    'new_col:string,updated_col:int64',
                    '--remove-columns',
                    'old_col',
                    '--merge-keys',
                    'id,new_col',
                ],
            )

            assert result.exit_code == 0
            mock_alter_table.assert_called_once()

    def test_alter_table_properties(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test altering table properties via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.catalog.main.impl.get_table') as mock_get_table,
            patch('deltacat.alter_table') as mock_alter_table,
            patch('deltacat.refresh_table') as mock_refresh_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_table.table_version.name = 'test_table'
            mock_table.table_version.schema = Mock()
            mock_get_table.return_value = mock_table

            result = runner.invoke(
                app,
                [
                    'table',
                    'alter',
                    '--name',
                    'test_table',
                    '--namespace',
                    namespace_name,
                    '--read-optimization-level',
                    'NONE',
                    '--records-per-compacted-file',
                    '8000000',
                ],
            )

            assert result.exit_code == 0
            mock_alter_table.assert_called_once()
            call_args = mock_alter_table.call_args
            table_properties = call_args.kwargs.get('table_properties')
            assert table_properties is not None

    def test_alter_table_error_handling(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test error handling in table alteration."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.catalog.main.impl.get_table') as mock_get_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_get_table.side_effect = TableNotFoundError('Table not found')

            result = runner.invoke(
                app,
                [
                    'table',
                    'alter',
                    '--name',
                    'nonexistent_table',
                    '--namespace',
                    namespace_name,
                    '--table-description',
                    'New description',
                ],
            )

            assert result.exit_code == 1
            assert 'Table not found' in result.output


class TestTableGetCLI:
    """Test the table get CLI command."""

    def test_get_table_success(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test successful table retrieval via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.get_table') as mock_get_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_table = Mock()
            mock_table.table.table_name = 'test_table'
            mock_get_table.return_value = mock_table

            result = runner.invoke(app, ['table', 'get', '--name', 'test_table', '--namespace', namespace_name])

            assert result.exit_code == 0
            mock_get_table.assert_called_once_with(table='test_table', namespace=namespace_name, catalog='test_catalog')

    def test_get_table_not_found(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test table not found scenario via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.get_table') as mock_get_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()
            mock_get_table.return_value = None

            result = runner.invoke(app, ['table', 'get', '--name', 'nonexistent_table', '--namespace', namespace_name])

            assert result.exit_code == 0
            assert 'No table with name nonexistent_table found' in result.output


class TestTableDropCLI:
    """Test the table drop CLI command."""

    def test_drop_table_success(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test successful table drop via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.drop_table') as mock_drop_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()

            result = runner.invoke(
                app, ['table', 'drop', '--name', 'test_table', '--namespace', namespace_name, '--drop'], input='y\ny\n'
            )  # Confirm both prompts

            assert result.exit_code == 0
            mock_drop_table.assert_called_once_with(
                table='test_table', namespace=namespace_name, catalog='test_catalog'
            )

    def test_drop_table_cancelled(self, runner: CliRunner, test_namespace: tuple[str, Any]) -> None:
        """Test cancelled table drop via CLI."""
        namespace_name, catalog_properties = test_namespace

        with (
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog_info') as mock_catalog_info,
            patch('deltacat_cli.utils.catalog_context.catalog_context.get_catalog') as mock_get_catalog,
            patch('deltacat.drop_table') as mock_drop_table,
        ):
            mock_catalog_info.return_value = ('test_catalog', catalog_properties)
            mock_get_catalog.return_value = Mock()

            result = runner.invoke(
                app, ['table', 'drop', '--name', 'test_table', '--namespace', namespace_name, '--drop'], input='n\n'
            )  # Cancel the operation

            assert result.exit_code == 1  # Typer exits with 1 when confirmation is cancelled
            mock_drop_table.assert_not_called()


class TestTablePropertiesUtils:
    """Test the TableProperties utility class."""

    def test_table_properties_creation_with_all_values(self) -> None:
        """Test TableProperties creation when all values are provided."""
        properties = TableProperties.of(
            read_optimization_level=TableReadOptimizationLevel.MAX,
            default_compaction_hash_bucket_count=16,
            records_per_compacted_file=5000000,
            appended_file_count_compaction_trigger=500,
            appended_delta_count_compaction_trigger=50,
            schema_evolution_mode=SchemaEvolutionMode.AUTO,
            default_schema_consistency_type=None,
        )

        assert properties.read_optimization_level == TableReadOptimizationLevel.MAX
        assert properties.default_compaction_hash_bucket_count == 16
        assert properties.records_per_compacted_file == 5000000
        assert properties.appended_record_count_compaction_trigger == 160000000  # 5000000 * 16 * 2
        assert properties.appended_file_count_compaction_trigger == 500
        assert properties.appended_delta_count_compaction_trigger == 50
        assert properties.schema_evolution_mode == SchemaEvolutionMode.AUTO

    def test_table_properties_creation_with_partial_values(self) -> None:
        """Test TableProperties creation when only some values are provided."""
        properties = TableProperties.of(
            read_optimization_level=TableReadOptimizationLevel.NONE,
            default_compaction_hash_bucket_count=None,
            records_per_compacted_file=1000000,
            appended_file_count_compaction_trigger=None,
            appended_delta_count_compaction_trigger=None,
            schema_evolution_mode=None,
            default_schema_consistency_type=None,
        )

        assert properties.read_optimization_level == TableReadOptimizationLevel.NONE
        assert properties.default_compaction_hash_bucket_count is None
        assert properties.records_per_compacted_file == 1000000
        # appended_record_count_compaction_trigger should not be set because default_compaction_hash_bucket_count is None
        assert properties.appended_record_count_compaction_trigger is None
        assert properties.appended_file_count_compaction_trigger is None
        assert properties.appended_delta_count_compaction_trigger is None
        assert properties.schema_evolution_mode is None

    def test_table_properties_creation_with_none_values(self) -> None:
        """Test TableProperties creation when records_per_compacted_file is None."""
        properties = TableProperties.of(
            read_optimization_level=None,
            default_compaction_hash_bucket_count=8,
            records_per_compacted_file=None,
            appended_file_count_compaction_trigger=None,
            appended_delta_count_compaction_trigger=None,
            schema_evolution_mode=None,
            default_schema_consistency_type=None,
        )

        assert properties.default_compaction_hash_bucket_count == 8
        assert properties.records_per_compacted_file is None
        # appended_record_count_compaction_trigger should not be set because records_per_compacted_file is None
        assert properties.appended_record_count_compaction_trigger is None


class TestTableSchemaUtils:
    """Test the table schema utility classes."""

    def test_table_schema_creation_from_string(self) -> None:
        """Test TableSchema creation from string."""
        schema_str = 'id:int64,name:string,created_at:timestamp[s]'
        schema = TableSchema.of(schema_str)

        assert len(schema) == 3
        assert schema['id'] == 'int64'
        assert schema['name'] == 'string'
        assert schema['created_at'] == 'timestamp[s]'

    def test_table_schema_creation_from_none(self) -> None:
        """Test TableSchema creation from None."""
        schema = TableSchema.of(None)
        assert len(schema) == 0

    def test_table_schema_creation_with_spaces(self) -> None:
        """Test TableSchema creation with spaces in field definitions."""
        schema_str = 'id : int64 , name : string , value : float64'
        schema = TableSchema.of(schema_str)

        assert len(schema) == 3
        assert schema['id'] == 'int64'
        assert schema['name'] == 'string'
        assert schema['value'] == 'float64'

    def test_deltacat_table_schema_creation(self) -> None:
        """Test DeltacatTableSchema creation."""
        table_schema = TableSchema.of('id:int64,name:string')
        merge_keys = 'id'

        with patch('deltacat_cli.utils.table_utils.DeltacatSchema.of') as mock_schema_of:
            mock_schema_of.return_value = Mock()

            result = DeltacatTableSchema.of(table_schema, merge_keys)

            mock_schema_of.assert_called_once()
            # Verify that the fields were created correctly
            call_args = mock_schema_of.call_args[0][0]  # First positional argument (fields list)
            assert len(call_args) == 2

    def test_deltacat_table_schema_creation_no_merge_keys(self) -> None:
        """Test DeltacatTableSchema creation without merge keys."""
        table_schema = TableSchema.of('id:int64,name:string')
        merge_keys = None

        with patch('deltacat_cli.utils.table_utils.DeltacatSchema.of') as mock_schema_of:
            mock_schema_of.return_value = Mock()

            result = DeltacatTableSchema.of(table_schema, merge_keys)

            mock_schema_of.assert_called_once()

    def test_create_schema_update_operations_add_only(self) -> None:
        """Test creating schema update operations with only additions."""
        operations = DeltacatTableSchema.create_schema_update_operations(schema_updates='new_field:string,age:int64')

        assert operations is not None
        # We can't easily test the internal structure without mocking,
        # but we can verify it was created successfully

    def test_create_schema_update_operations_remove_only(self) -> None:
        """Test creating schema update operations with only removals."""
        operations = DeltacatTableSchema.create_schema_update_operations(remove_columns='old_field,deprecated_col')

        assert operations is not None

    def test_create_schema_update_operations_add_and_remove(self) -> None:
        """Test creating schema update operations with both additions and removals."""
        operations = DeltacatTableSchema.create_schema_update_operations(
            schema_updates='new_field:string,updated_field:int64', remove_columns='old_field,temp_column'
        )

        assert operations is not None

    def test_create_schema_update_operations_none(self) -> None:
        """Test creating schema update operations with no parameters."""
        operations = DeltacatTableSchema.create_schema_update_operations()

        assert operations is None

    def test_create_schema_update_operations_empty_strings(self) -> None:
        """Test creating schema update operations with empty strings."""
        operations = DeltacatTableSchema.create_schema_update_operations(schema_updates='', remove_columns='')

        assert operations is None
