import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.bip122 import Bip122Uri

GENESIS_HASH = "d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3"
BLOCK_HASH = "752820c0ad7abc1200f9ad42c4adc6fbb4bd44b5bed4667990e64565102c1ba6"
EXAMPLE = f"blockchain://{GENESIS_HASH}/block/{BLOCK_HASH}"


class Model(BaseModel):
    uri: Bip122Uri


def test_bip122():
    model = Model(uri=EXAMPLE)
    assert model.uri == EXAMPLE


@pytest.mark.parametrize(
    "uri",
    (
        "foo",
        f"blockchain://foo/block/{BLOCK_HASH}",
        f"blockchain://{GENESIS_HASH}/block/foo",
        f"blockchain://{GENESIS_HASH}/tx/foo",
    ),
)
def test_invalid_bip122(uri):
    with pytest.raises(ValidationError):
        Model(uri=uri)


def test_schema():
    actual = Model.model_json_schema()
    prop = actual["properties"]["uri"]
    assert prop["type"] == "string"
    assert prop["title"] == "Uri"
    assert prop["examples"] == [EXAMPLE]
    assert prop["pattern"] == "^blockchain://[0-9a-f]{64}/block/[0-9a-f]{64}$"
