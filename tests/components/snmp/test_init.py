"""SNMP tests."""

from unittest.mock import patch

from pysnmp.hlapi.v3arch.asyncio import SnmpEngine
from pysnmp.hlapi.v3arch.asyncio.cmdgen import LCD

from universalassistant.components import snmp
from universalassistant.const import EVENT_HOMEASSISTANT_STOP
from universalassistant.core import __HAC_KEEP__


async def test_async_get_snmp_engine(hass: __HAC_KEEP__) -> None:
    """Test async_get_snmp_engine."""
    engine = await snmp.async_get_snmp_engine(hass)
    assert isinstance(engine, SnmpEngine)
    engine2 = await snmp.async_get_snmp_engine(hass)
    assert engine is engine2
    with patch.object(LCD, "unconfigure") as mock_unconfigure:
        hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
        await hass.async_block_till_done()
    assert mock_unconfigure.called
