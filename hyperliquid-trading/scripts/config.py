"""Configuration management for Hyperliquid CLI."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class HyperliquidConfig:
    """Hyperliquid configuration."""

    network: str = "testnet"
    account_address: Optional[str] = None
    secret_key: Optional[str] = None
    api_secret_key: Optional[str] = None
    log_level: str = "INFO"
    language: str = "en"

    @property
    def is_mainnet(self) -> bool:
        """Check if using mainnet."""
        return self.network.lower() == "mainnet"

    @property
    def api_url(self) -> str:
        """Get API URL based on network."""
        if self.is_mainnet:
            return "https://api.hyperliquid.xyz"
        return "https://api.hyperliquid-testnet.xyz"

    def validate(self, require_auth: bool = True) -> list[str]:
        """Validate configuration and return list of errors.

        Args:
            require_auth: If True, requires secret_key for validation
        """
        errors = []
        if not self.account_address:
            errors.append("HL_ACCOUNT_ADDRESS is required")
        if require_auth and not self.secret_key and not self.api_secret_key:
            errors.append("HL_SECRET_KEY is required for trading operations")
        return errors


def load_config(env_file: Optional[str] = None) -> HyperliquidConfig:
    """Load configuration from environment variables.

    Args:
        env_file: Optional path to .env file

    Returns:
        HyperliquidConfig instance
    """
    # Load from .env file if provided or exists
    if env_file:
        load_dotenv(env_file)
    else:
        # Try to find .env in current directory and project root
        cwd_env = Path(".env")
        if cwd_env.exists():
            load_dotenv(cwd_env)
        else:
            project_root = Path(__file__).parent.parent
            root_env = project_root / ".env"
            if root_env.exists():
                load_dotenv(root_env)

    return HyperliquidConfig(
        network=os.getenv("HL_NETWORK", "testnet"),
        account_address=os.getenv("HL_ACCOUNT_ADDRESS"),
        secret_key=os.getenv("HL_SECRET_KEY"),
        api_secret_key=os.getenv("HL_API_SECRET_KEY"),
        log_level=os.getenv("HL_LOG_LEVEL", "INFO"),
        language=os.getenv("HL_LANGUAGE", "en"),
    )


def setup_config_interactive() -> HyperliquidConfig:
    """Interactive configuration setup."""
    print("Hyperliquid CLI Configuration Setup")
    print("=" * 40)

    network = input("Network (mainnet/testnet) [testnet]: ").strip() or "testnet"
    account_address = input("Your wallet address (0x...): ").strip()
    secret_key = input("Your private key (0x...): ").strip()
    api_secret_key = input("API wallet private key (optional): ").strip() or None
    log_level = input("Log level (DEBUG/INFO/WARNING/ERROR) [INFO]: ").strip() or "INFO"
    language = input("Language (en/zh-CN) [en]: ").strip() or "en"

    config = HyperliquidConfig(
        network=network,
        account_address=account_address,
        secret_key=secret_key,
        api_secret_key=api_secret_key,
        log_level=log_level,
        language=language,
    )

    # Save to .env file
    env_content = f"""# Hyperliquid API Configuration
HL_NETWORK={network}
HL_ACCOUNT_ADDRESS={account_address}
HL_SECRET_KEY={secret_key}
"""
    if api_secret_key:
        env_content += f"HL_API_SECRET_KEY={api_secret_key}\n"
    env_content += f"HL_LOG_LEVEL={log_level}\n"
    env_content += f"HL_LANGUAGE={language}\n"

    env_path = Path(".env")
    with open(env_path, "w") as f:
        f.write(env_content)

    print(f"\nConfiguration saved to {env_path.absolute()}")
    return config
