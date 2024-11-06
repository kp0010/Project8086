mov ax, bx
sub dx, bx
add cl, ah
mov ax, [0xf0 + 0x0f]
mov [0x100], dx
hlt
