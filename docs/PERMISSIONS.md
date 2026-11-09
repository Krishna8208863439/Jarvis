# Project NOVA: Permissions Model

## Permission Categories
1. `microphone`: Audio streaming for speech recognition and local wake word.
2. `device.info`: Reading battery, OS version, and network status.
3. `device.apps`: Launching installed applications via platform schemes or execution registry.
4. `device.shell`: Execution of strictly allowlisted terminal commands with argument validation.
5. `device.files`: Reading and writing within user-approved directories.
6. `device.notifications`: Scheduling and displaying native system notifications.

## Revocation & Audit
- Users may revoke any granted permission per registered device at any time.
- Every permission-gated action generates a signed entry in the immutable `audit_logs` table.

