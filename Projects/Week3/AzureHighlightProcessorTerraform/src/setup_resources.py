def update_env_file(connection_string):
    """Update the .env file and azure_storage_connection_string.txt with the new connection string."""
    env_file = ".env"
    env_lines = []

    # Read existing .env file (if it exists)
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            env_lines = f.readlines()

    # Update or add the AZURE_STORAGE_CONNECTION_STRING variable
    found = False
    for i, line in enumerate(env_lines):
        if line.startswith("AZURE_STORAGE_CONNECTION_STRING="):
            env_lines[i] = f"AZURE_STORAGE_CONNECTION_STRING={connection_string}\n"
            found = True
    if not found:
        env_lines.append(f"\nAZURE_STORAGE_CONNECTION_STRING={connection_string}\n")

    # Write back to .env file
    with open(env_file, "w") as f:
        f.writelines(env_lines)

    # Additionally, write the connection string to a separate file
    with open("azure_storage_connection_string.txt", "w") as f:
        f.write(connection_string)

    print("Updated .env file and azure_storage_connection_string.txt with the new AZURE_STORAGE_CONNECTION_STRING.")
