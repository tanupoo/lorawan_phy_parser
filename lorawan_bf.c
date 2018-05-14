/*
 * Copyright(C) 2000-2017 Shoichi Sakane <sakane@tanu.org>, All rights reserved.
 * See the file LICENSE in the top level directory for more details.
 */
/*
 * cc -O3 lorawan_bf.c -o lorawan_bf -lcrypto
 */
#include <sys/types.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <err.h>
#include <openssl/aes.h>

uint8_t key[16];
uint8_t out[16];
uint8_t src[16];

int f_debug = 0;

char *prog_name = NULL;

void
usage()
{
	printf(
"Usage: %s [-dh] (data) [key]\n"
"       %s [-dh] -t (data)\n"
"    -t: specify to do a dictionary trial.  if not, do a brute force tiral.\n"
"    data: encrypted data in hex.\n"
"    key : key in hex to be started. default is 0.\n"
	, prog_name, prog_name);

	exit(0);
}

void
dump16(char *prefix, uint8_t *data)
{
	printf("%s", prefix);
	for (int i = 0; i < 16; i++) {
		printf("%02x", data[i]);
	}
	printf("\n");
}

void
sig_handle(int sig)
{
	printf("signal %dn was caught\n", sig);
	dump16("key=", key);
	printf("\n");
	fflush(stdout);
	exit(0);
}

void
sig_set(int sig)
{
	if (SIG_ERR == signal(sig, sig_handle))
		errx(1, "failed to set signal handler.n");
}

void
a2b_hex16(char *data_hex, uint8_t *data)
{
	for (int i = 0; i < 32; i+=2) {
		char *bp;
		char buf[3];
		buf[0] = (uint8_t)data_hex[i];
		buf[1] = (uint8_t)data_hex[i+1];
		buf[2] = '\0';
		data[i/2] = (uint8_t)strtol(buf, &bp, 16);
		if (*bp != '\0')
			errx(1, "ERROR: invalid char %02x", (uint8_t)*bp);
	}
}

int
increment()
{
	for (int i = 15; i >= 0; i--) {
		if (key[i] != 0xff) {
			key[i]++;
			//dump16("key=", key);
			return 0;
		}
		if (i == 0) {
			/*
			 * return 1, when all 16 bytes are 0xff
			 */
			return 1;
		}
		key[i] = 0;
	}
	errx(1, "ERROR: never come in.");
}

void
check()
{
	/*
	 * AppNonce |   NetID  |   DevAddr   | DL | RD | [CFList] | MIC)
	 *
	 * AppNonce |   NetID  |   DevAddr   | DL | RD |     MIC
	 * -- -- -- | zz 00 00 | -- -- -- -- | zz | 01 | -- -- -- --
	 * 75 5e 06   15 00 00   fd 18 17 2b   02   01   c3 28 61 84
	 *
	 * ## NetID
	 * Any choices           | NwkID
	 * ---- ---- ---- ---- - | 000 0000
	 *
	 * ## NwkID
	 * 000 0000: Free
	 * 000 0001: Semtech ?
	 * 000 0010: Actility
	 * 000 1111: Cisco
	 *
	 * ## DL (DLSettings)
	 * RFU | RX1DRoffset | RX2 Data rate
	 * 7   | 6 5 4       | 3 2 1 0
	 *
	 * RX2 DR default is 2 in AS923.
	 * RX1 Delay default is 1 in AS923.
	 */
	if (out[4] == 0 && out[5] == 0 &&
	    out[10] == 0x02 && out[11] == 0x01 &&
	    (out[3] == 0x00 ||
	     out[3] == 0x01 ||
	     out[3] == 0x02 ||
	     out[3] == 0x15)) {
		dump16("key=", key);
		dump16("out=", out);
	}
}

void
lorawan_decrypt()
{
	/*
	 * AES ECB encrypt
	 * LoRaWAN always uses AES-ECB encryption
	 * to encrypt or decrypto data.
	 */
	AES_KEY aes_key;
	AES_set_encrypt_key(key, 128, &aes_key);
	AES_ecb_encrypt(src, out, &aes_key, AES_ENCRYPT);
	//dump16("out=", out);
}

void
dt_repeat_8()
{
	/* 0x00 ... 0xff x 16 */
	for (int i = 0; i <= 0xff; i++) {
		for (int j = 0; j < 16; j++) {
			key[j] = (uint8_t)(i&0xff);
		}
		if (f_debug)
			dump16("dict_key=", key);
		lorawan_decrypt();
		check();
	}
}

void
dt_repeat_16()
{
	/* 0x0000, 0x0101, 0x0202 ... 0xfefe, 0xffff x 8 */
	int v[] = {
		0x0102,

		0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007, 0x0008,
		0x0009, 0x000a, 0x000b, 0x000c, 0x000d, 0x000e, 0x000f,

		0x0011, 0x0022, 0x0033, 0x0044, 0x0055, 0x0066, 0x0077, 0x0088,
		0x0099, 0x00aa, 0x00bb, 0x00cc, 0x00dd, 0x00ee, 0x00ff,

		0x1000, 0x2000, 0x3000, 0x4000, 0x5000, 0x6000, 0x7000, 0x8000,
		0x9000, 0xa000, 0xb000, 0xc000, 0xd000, 0xe000, 0xf000,

		0x1100, 0x2200, 0x3300, 0x4400, 0x5500, 0x6600, 0x7700, 0x8800,
		0x9900, 0xaa00, 0xbb00, 0xcc00, 0xdd00, 0xee00, 0xff00,
	};
	for (int i = 0; i < sizeof(v); i++) {
		for (int j = 0; j < 16; j+=2) {
			key[j] = (uint8_t)((v[i]>>8)&0xff);
			key[j+1] = (uint8_t)(v[i]&0xff);
		}
		if (f_debug)
			dump16("dict_key=", key);
		lorawan_decrypt();
		check();
	}
}

void
dt_repeat_32()
{
	int v[] = {
		0x00000001, 0x00000002, 0x00000003, 0x00000004,
		0x00000005, 0x00000006, 0x00000007, 0x00000008,
		0x00000009, 0x0000000a, 0x0000000b, 0x0000000c,
		0x0000000d, 0x0000000e, 0x0000000f,

		0x10000000, 0x20000000, 0x30000000, 0x40000000,
		0x50000000, 0x60000000, 0x70000000, 0x80000000,
		0x90000000, 0xa0000000, 0xb0000000, 0xc0000000,
		0xd0000000, 0xe0000000, 0xf0000000,
	};
	for (int i = 0; i < sizeof(v); i++) {
		for (int j = 0; j < 16; j+=4) {
			key[j]   = (uint8_t)((v[i]>>24)&0xff);
			key[j+1] = (uint8_t)((v[i]>>16)&0xff);
			key[j+2] = (uint8_t)((v[i]>> 8)&0xff);
			key[j+3] = (uint8_t)(v[i]&0xff);
		}
		if (f_debug)
			dump16("dict_key=", key);
		lorawan_decrypt();
		check();
	}
}

void
dt_set_01()
{
	int v[] = { 0x11112222, 0x33334444, 0x55556666, 0x77778888, };
	for (int i = 0; i < sizeof(v); i++) {
		key[i*4]   = (uint8_t)((v[i]>>24)&0xff);
		key[i*4+1] = (uint8_t)((v[i]>>16)&0xff);
		key[i*4+2] = (uint8_t)((v[i]>> 8)&0xff);
		key[i*4+3] = (uint8_t)(v[i]&0xff);
	}
	if (f_debug)
		dump16("dict_key=", key);
	lorawan_decrypt();
	check();
}

void
dt_set_02()
{
	int v[] = { 0x00001111, 0x22223333, 0x44445555, 0x66667777, };
	for (int i = 0; i < sizeof(v); i++) {
		key[i*4]   = (uint8_t)((v[i]>>24)&0xff);
		key[i*4+1] = (uint8_t)((v[i]>>16)&0xff);
		key[i*4+2] = (uint8_t)((v[i]>> 8)&0xff);
		key[i*4+3] = (uint8_t)(v[i]&0xff);
	}
	if (f_debug)
		dump16("dict_key=", key);
	lorawan_decrypt();
	check();
}

void
dt_set_03()
{
	int v[] = { 0x11111111, 0x22222222, 0x33333333, 0x44444444, };
	for (int i = 0; i < sizeof(v); i++) {
		key[i*4]   = (uint8_t)((v[i]>>24)&0xff);
		key[i*4+1] = (uint8_t)((v[i]>>16)&0xff);
		key[i*4+2] = (uint8_t)((v[i]>> 8)&0xff);
		key[i*4+3] = (uint8_t)(v[i]&0xff);
	}
	if (f_debug)
		dump16("dict_key=", key);
	lorawan_decrypt();
	check();
}

void
dt_set_fixed()
{
	char *sv[] = { "00112233445566778899aabbccddeeff" };
	for (int i = 0; i < sizeof(sv)/sizeof(sv[0]); i++) {
		a2b_hex16(sv[i], key);
		if (f_debug)
			dump16("dict_key=", key);
		lorawan_decrypt();
		check();
	}
}

int
dict_trial()
{
	dt_repeat_8();
	dt_repeat_16();
	dt_repeat_32();
	dt_set_01();
	dt_set_02();
	dt_set_03();
	dt_set_fixed();

	return 0;
}

int
bf_trial()
{
	memset(out, 0, 16);

	for (int i = 0; i <= 0xffffffff; i++) {
		printf("#%08x\n", i);
		for (int j = 0; j <= 0xffffffff; j++) {
			lorawan_decrypt();
			check();
			if (increment())
				break;
			//dump16("key=", key);
		}
	}

	return 0;
}

int
main(int argc, char *argv[])
{
	int ch;
	int f_dict_trial = 0;

	prog_name = 1 + rindex(argv[0], '/');

	while ((ch = getopt(argc, argv, "dht")) != -1) {
		switch (ch) {
		case 't':
			f_dict_trial++;
			break;
		case 'd':
			f_debug++;
			break;
		case 'h':
		default:
			usage();
			break;
		}
	}
	argc -= optind;
	argv += optind;

	memset(key, 0, 16);
	switch (argc) {
	case 2:
		a2b_hex16(argv[1], key);
		dump16("init key=", key);
	case 1:
		/*
		char *data_hex = "eec723f2622b015c0b701ae7bda0c23d";
		*/
		a2b_hex16(argv[0], src);
		dump16("src data=", src);
		break;
	default:
		usage();
	}

	sig_set(SIGINT);

	if (f_dict_trial) {
		printf("Dictionary Trial:\n");
		dict_trial();
	} else {
		printf("Brute Force:\n");
		bf_trial();
	}

	return 0;
}

