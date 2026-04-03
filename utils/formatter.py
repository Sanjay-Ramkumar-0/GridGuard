def format_output(errors, warnings, suggestions):
    print("\n" + "="*50)
    print("🔷 GRIDGUARD REPORT")
    print("="*50)

    # Errors
    if errors:
        print("\n❌ ERRORS:")
        for e in errors:
            print(f"- {e}")
    else:
        print("\n✅ No critical errors")

    # Warnings
    if warnings:
        print("\n⚠️ WARNINGS:")
        for w in warnings:
            print(f"- {w}")

    # Suggestions
    if suggestions:
        print("\n💡 SUGGESTIONS:")
        for s in suggestions:
            print(f"- {s}")

    print("\n" + "="*50)