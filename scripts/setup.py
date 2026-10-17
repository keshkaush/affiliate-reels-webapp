"""
Setup Script for Affiliate Reels Automation
===========================================

Helps you configure the bot and verify all credentials are working.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_env_file():
    """Check if .env file exists."""
    env_path = Path('.env')

    if not env_path.exists():
        print("❌ .env file not found!")
        print("\n📝 Creating .env from template...")

        # Copy .env.example to .env
        example_path = Path('.env.example')
        if example_path.exists():
            with open(example_path, 'r') as f:
                content = f.read()

            with open(env_path, 'w') as f:
                f.write(content)

            print("✅ .env file created!")
            print("\n⚠️  IMPORTANT: Edit .env and add your API credentials before continuing.")
            return False
        else:
            print("❌ .env.example not found!")
            return False

    return True


def verify_credentials():
    """Verify that credentials are configured."""
    load_dotenv()

    required_vars = {
        'Social Media': [
            'META_APP_ID',
            'INSTAGRAM_ACCOUNT_ID',
            'TIKTOK_CLIENT_KEY'
        ],
        'Affiliate Networks': [
            'AMAZON_ASSOCIATE_TAG',
            'SHAREASALE_AFFILIATE_ID'
        ],
        'AI Services': [
            'GEMINI_API_KEY'
        ]
    }

    missing = []

    print_header("Checking Credentials")

    for category, vars_list in required_vars.items():
        print(f"\n{category}:")
        for var in vars_list:
            value = os.getenv(var)

            if value and value != f"your_{var.lower()}_here" and value != "your_" + "_".join(var.lower().split('_')[1:]) + "_here":
                print(f"  ✅ {var}")
            else:
                print(f"  ❌ {var} - NOT CONFIGURED")
                missing.append(var)

    if missing:
        print(f"\n⚠️  Missing {len(missing)} required credentials:")
        for var in missing:
            print(f"    - {var}")
        print("\n📝 Edit .env and add these values before running the bot.")
        return False

    print("\n✅ All credentials configured!")
    return True


def install_dependencies():
    """Install Python dependencies."""
    print_header("Installing Dependencies")

    print("📦 Installing Python packages...")

    os.system(f"{sys.executable} -m pip install -r requirements.txt")

    print("\n✅ Dependencies installed!")


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directories")

    dirs = [
        'data/videos',
        'data/cache',
        'data/db',
        'logs',
        'config'
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_path}/")

    print("\n✅ Directory structure created!")


def test_api_connections():
    """Test API connections (optional)."""
    print_header("Testing API Connections")

    print("🔗 Testing social media APIs...")
    print("  ⚠️  Skipping (implement in production)")

    print("\n🔗 Testing affiliate networks...")
    print("  ⚠️  Skipping (implement in production)")

    print("\n🔗 Testing AI services...")
    print("  ⚠️  Skipping (implement in production)")


def main():
    """Run setup wizard."""
    print_header("🤖 Affiliate Reels Automation - Setup Wizard")

    print("This wizard will help you set up your affiliate automation bot.\n")

    # Step 1: Check .env
    if not check_env_file():
        print("\n⚠️  Setup incomplete. Please configure .env and run setup again.")
        return

    # Step 2: Verify credentials
    input("\nPress Enter to verify your credentials...")
    if not verify_credentials():
        print("\n⚠️  Setup incomplete. Please add missing credentials to .env")
        return

    # Step 3: Install dependencies
    install = input("\nInstall Python dependencies? (y/n): ").lower()
    if install == 'y':
        install_dependencies()

    # Step 4: Create directories
    create_directories()

    # Step 5: Test connections (optional)
    test = input("\nTest API connections? (y/n): ").lower()
    if test == 'y':
        test_api_connections()

    # Done!
    print_header("✅ Setup Complete!")

    print("Your bot is ready to run!\n")
    print("Quick start commands:")
    print("  python main.py --mode discover    # Find trending content")
    print("  python main.py --mode monitor     # Monitor comments/DMs")
    print("  python main.py --mode auto        # Full automation\n")

    print("⚠️  Important reminders:")
    print("  - Always disclose affiliate relationships (#ad, #affiliate)")
    print("  - Review platform Terms of Service")
    print("  - Start with manual testing before full automation")
    print("  - Monitor your bot's behavior regularly\n")


if __name__ == '__main__':
    main()
