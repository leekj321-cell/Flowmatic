# Flowmatic Branding Rollback

The version immediately before the visual identity update is preserved in two forms:

- Git tag: `backup/pre-branding-20260803`
- ZIP archive: `../backups/flowmatic-pre-branding-20260803-088462f5ed24.zip`
- SHA-256 file: `../backups/flowmatic-pre-branding-20260803-088462f5ed24.zip.sha256`

When rollback is requested, prefer a normal Git revert of the branding deployment commit so history stays intact. The tag and ZIP provide independent recovery points if the deployed commit is unavailable.
