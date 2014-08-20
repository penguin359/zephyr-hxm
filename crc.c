#include <stdint.h>

void crc8PushByte(uint8_t *crc, uint8_t ch)
{
	uint8_t i;
	*crc = *crc ^ ch;
	for (i=0; i<8; i++)
	{
		if (*crc & 1)
		{
			*crc = (*crc >> 1) ^0x8C;
		}
		else
		{
			*crc = (*crc >> 1);
		}
	}
}

uint8_t crc8PushBlock(uint8_t *pcrc, uint8_t *block
		, uint16_t count)
{
	uint8_t crc = pcrc ? *pcrc : 0;
	for (; count>0; --count,block++)
	{
		crc8PushByte(&crc, *block);
	}
	if (pcrc) *pcrc = crc;
	return crc;
}
