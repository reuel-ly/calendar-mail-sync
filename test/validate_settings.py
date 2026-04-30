import sys


def validate_settings():
    """Validate all settings can be imported and have valid values."""
    errors = []
    warnings = []

    print("=" * 60)
    print("Validating core/settings.py")
    print("=" * 60)

    # Step 1: Check module imports
    print("\n[1] Checking module imports...")
    try:
        from pydantic_settings import BaseSettings
        print("    ✓ pydantic_settings.BaseSettings imported")
    except ImportError as e:
        errors.append(f"Failed to import pydantic_settings: {e}")
        print(f"    ✗ Failed to import pydantic_settings: {e}")
        return errors, warnings

    # Step 2: Import the settings module
    print("\n[2] Importing settings module...")
    try:
        from core.settings import AgentSettings, settings
        print("    ✓ AgentSettings class imported")
        print("    ✓ settings instance created")
    except ImportError as e:
        errors.append(f"Failed to import settings module: {e}")
        print(f"    ✗ Failed to import settings module: {e}")
        return errors, warnings
    except Exception as e:
        errors.append(f"Error initializing settings: {e}")
        print(f"    ✗ Error initializing settings: {e}")
        return errors, warnings

    # Step 3: Validate settings instance
    print("\n[3] Validating settings instance...")

    # Check that settings is an AgentSettings instance
    if not isinstance(settings, AgentSettings):
        errors.append("settings is not an AgentSettings instance")
        print("    ✗ settings is not an AgentSettings instance")
    else:
        print("    ✓ settings is a valid AgentSettings instance")

    # Step 4: Check all expected fields exist and have values
    print("\n[4] Checking all expected fields...")
    expected_fields = [
        "default_model",
        "school_email_model",
        "school_email_instruction",
        "work_email_model",
        "work_email_instruction",
        "personal_email_model",
        "personal_email_instruction",
        "calendar_model",
        "calendar_instruction",
        "summarizer_model",
        "summarizer_instruction",
        "discord_model",
        "discord_instruction",
    ]

    for field in expected_fields:
        if not hasattr(settings, field):
            errors.append(f"Missing field: {field}")
            print(f"    ✗ Missing field: {field}")
        else:
            value = getattr(settings, field)
            if value is None:
                warnings.append(f"Field '{field}' is None (using default or not set)")
                print(f"    ⚠ {field} = None")
            elif isinstance(value, str) and not value.strip():
                errors.append(f"Field '{field}' is empty string")
                print(f"    ⚠ {field} = '' (empty)")
            else:
                print(f"    ✓ {field} = {repr(value)[:50]}...")

    # Step 5: Validate instruction fields have content
    print("\n[5] Validating instruction fields...")
    instruction_fields = [
        "school_email_instruction",
        "work_email_instruction",
        "personal_email_instruction",
        "calendar_instruction",
        "summarizer_instruction",
        "discord_instruction",
    ]

    for field in instruction_fields:
        value = getattr(settings, field, None)
        if value and len(value.strip()) < 20:
            warnings.append(f"Instruction '{field}' seems too short ({len(value)} chars)")
            print(f"    ⚠ {field} is short ({len(value)} chars)")
        elif value:
            print(f"    ✓ {field} ({len(value)} chars)")

    # Step 6: Check model settings
    print("\n[6] Validating model settings...")
    if settings.default_model:
        print(f"    ✓ default_model = '{settings.default_model}'")
    else:
        warnings.append("default_model is not set")
        print("    ⚠ default_model is not set")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if errors:
        print(f"\n❌ ERRORS: {len(errors)}")
        for err in errors:
            print(f"   - {err}")
    else:
        print("\n✓ No errors")

    if warnings:
        print(f"\n⚠ WARNINGS: {len(warnings)}")
        for warn in warnings:
            print(f"   - {warn}")
    else:
        print("\n✓ No warnings")

    print("\n" + "=" * 60)

    if errors:
        print("RESULT: FAILED - Fix errors above")
        return errors, warnings
    else:
        print("RESULT: PASSED - All settings validated successfully")
        return errors, warnings


if __name__ == "__main__":
    errors, warnings = validate_settings()
    sys.exit(1 if errors else 0)
