//gba.h

//Building a game, we are drawing to screen
//240x160
//16 bit color word
//Xbbbbbgggggrrrrr
//Thumb instructions (16 bit)

//0x00000000 -> 0x00003fff (System ROM, exec but not readable)
//0x02000000 -> 0x02020000 (External to the CPU RAM, 256 KB)
//0x03000000 -> 0x03007fff (Internal to the CPU RAM, 32 KB)
//0x04000000 -> 0x040003ff (IO Registers)
//0x05000000 -> 0x050003ff (Color Palette)
//0x06000000 -> 0x06017fff (Video RAM, 96 KB)
//0x07000000 -> 0x070003ff (Object Attribute Memory)
//0x08000000 -> 0x???????? (Gamepak ROM size (up to 32 MB))
//0x0E000000 -> 0x???????? (Gamepak RAM)

#define SCREEN_HEIGHT   160
#define SCREEN_WIDTH    240

typedef unsigned short  uint16;
typedef unsigned int    uint32;

#define MEMIO           0x04000000
#define VRAM            0x06000000

#define VIDEOMODE       0x0003
#define BGMODE          0x0400

#define REG_DISPLAY         (*(volatile uint32 *)(MEMIO))
#define REG_DISPLAY_VCOUNT  (*(volatile uint32 *)(MEMIO + 0x0006))
#define REG_DISPLAY_INPUT   (*(volatile uint32 *)(MEMIO + 0x0130))

#define SCREENBUFFER        ((volatile uint16 *) VRAM)














