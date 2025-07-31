# PyPI Publishing Guide for pycoreux

This guide explains how to publish pycoreux to PyPI using GitHub Actions and manual methods.

## Prerequisites

1. **PyPI Account**: Create accounts at:
   - [PyPI](https://pypi.org/) (production)
   - [TestPyPI](https://test.pypi.org/) (testing)

2. **API Tokens**: Generate API tokens for both PyPI and TestPyPI
   - Go to Account Settings → API tokens
   - Create tokens with appropriate permissions

## Method 1: Automated Publishing via GitHub Actions

### Setup GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `PYPI_API_TOKEN`: Your PyPI API token
   - `TEST_PYPI_API_TOKEN`: Your TestPyPI API token

### Publishing Workflow

#### Test Release (TestPyPI)
```bash
# Trigger manual workflow for testing
1. Go to Actions tab in GitHub
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Select "testpypi" environment
5. Click "Run workflow"
```

#### Production Release
```bash
# Create a new release tag
git tag v0.1.0
git push origin v0.1.0

# Or create release through GitHub UI
1. Go to Releases → Create a new release
2. Choose a tag (e.g., v0.1.0)
3. Fill in release notes
4. Publish release
```

## Method 2: Manual Publishing

### Install Dependencies
```bash
pip install build twine
```

### Build Package
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build
```

### Test on TestPyPI
```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ pycoreux
```

### Publish to PyPI
```bash
# Upload to production PyPI
python -m twine upload dist/*
```

## Version Management

### Update Version
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit changes
4. Create new tag: `git tag v0.1.1`
5. Push tag: `git push origin v0.1.1`

### Pre-release Versions
```bash
# For alpha/beta releases
git tag v0.2.0a1  # Alpha
git tag v0.2.0b1  # Beta
git tag v0.2.0rc1 # Release candidate
```

## Verification

### Check Package on PyPI
- Visit: https://pypi.org/project/pycoreux/
- Verify metadata, description, and links

### Test Installation
```bash
# Install from PyPI
pip install pycoreux

# Test basic functionality
python -c "from pycoreux import FileOps; print('✅ Import successful')"
```

## Troubleshooting

### Common Issues

1. **Package name already exists**: Choose a different name in `pyproject.toml`
2. **Invalid metadata**: Check `pyproject.toml` syntax
3. **Upload errors**: Verify API tokens are correct
4. **Version conflicts**: Ensure version number is incremented

### Build Issues
```bash
# Check package before upload
python -m twine check dist/*

# Validate pyproject.toml
python -m build --check
```

## Security Best Practices

1. **Never commit API tokens** to version control
2. **Use GitHub Secrets** for storing sensitive data
3. **Limit token scope** to minimum required permissions
4. **Regularly rotate tokens** for security

## Automation Tips

### Auto-increment Version
Add this to your workflow:
```yaml
- name: Bump version
  run: |
    # Use bump2version or similar tool
    pip install bump2version
    bump2version patch  # or minor, major
```

### Release Notes Generation
```yaml
- name: Generate Release Notes
  uses: actions/github-script@v6
  with:
    script: |
      // Auto-generate release notes from commits
```

## Publishing Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run tests locally: `pytest`
- [ ] Check code formatting: `black . && isort .`
- [ ] Build package: `python -m build`
- [ ] Test on TestPyPI first
- [ ] Create GitHub release
- [ ] Verify on PyPI
- [ ] Test installation: `pip install pycoreux`
- [ ] Update documentation if needed
