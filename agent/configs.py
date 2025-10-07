from pydantic_settings import BaseSettings, SettingsConfigDict


class SgxConfig(BaseSettings):
    sgx_url: str
    ecdsa_key_name: str
    bls_key_name: str
    sgx_ssl_key_path: str
    sgx_ssl_cert_path: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


class Config(BaseSettings):
    mainnet_endpoint: str
    schain_endpoint: str
    ima_contracts: str
    manager_contracts: str
    schain_name: str

    ima_contracts_schain: str = 'predeployed'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


config = Config()  # type: ignore[call-arg]
sgx_config = SgxConfig()  # type: ignore[call-arg]
