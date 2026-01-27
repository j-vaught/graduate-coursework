//main.c

#include "gba.h"

void sync()
{
    //always draw in vbuffer
    while(REG_DISPLAY_VCOUNT >= 160);
    while(REG_DISPLAY_VCOUNT < 160);
}

int main()
{
    REG_DISPLAY = VIDEOMODE | BGMODE;

    int inc = 0;
    int clearline = 0;
    while(1)
    {
        sync();

        SCREENBUFFER[clearline * 240 + 110] = 0x0000;
        SCREENBUFFER[clearline * 240 + 120] = 0x0000;
        SCREENBUFFER[clearline * 240 + 130] = 0x0000;

        //draw our pixels
        SCREENBUFFER[inc * 240 + 110] = 0x001f;
        SCREENBUFFER[inc * 240 + 120] = 0x03e0;
        SCREENBUFFER[inc * 240 + 130] = 0x7c00;

        clearline = inc;
        inc++;
        if(inc == 160)
            inc = 0;
    }
    return 0;
}