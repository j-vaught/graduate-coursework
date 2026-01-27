module test (
	input CLOCK_50,
	input [3:0] KEY, 
	input [1:0] SW, 
	output [12:0] DRAM_ADDR,
	output [1:0] DRAM_BA,
	output DRAM_CAS_N,
	output DRAM_CKE,
	output DRAM_CS_N,
	inout [31:0] DRAM_DQ,
	output [3:0] DRAM_DQM,
	output DRAM_RAS_N,
	output DRAM_WE_N,
	output DRAM_CLK,
	output VGA_CLK,
	output VGA_HS,
	output VGA_VS,
	output VGA_BLANK_N,
	output VGA_SYNC_N,
	output [7:0] VGA_R,
	output [7:0] VGA_G,
	output [7:0] VGA_B,
	inout [15:0] SRAM_DQ,
	output [19:0] SRAM_ADDR,
	output SRAM_LB_N,
	output SRAM_UB_N,
	output SRAM_CE_N,
	output SRAM_OE_N,
	output SRAM_WE_N);
	
	nios_system u0 (
	.clk_clk (CLOCK_50),
	.reset_reset_n (KEY[0]),
	//modes_export (SW),
	.sdram_clk_clk (DRAM_CLK), // sdram_clk.clk
	.sdram_addr (DRAM_ADDR), // sdram.addr
	.sdram_ba (DRAM_BA), // .ba
	.sdram_cas_n (DRAM_CAS_N), // .cas_n
	.sdram_cke (DRAM_CKE), // .cke
	.sdram_cs_n (DRAM_CS_N), // .cs_n
	.sdram_dq (DRAM_DQ), // .dq
	.sdram_dqm (DRAM_DQM), // .dqm
	.sdram_ras_n (DRAM_RAS_N), // .ras_n
	.sdram_we_n (DRAM_WE_N),
	.vga_CLK (VGA_CLK), // vga.CLK
	.vga_HS (VGA_HS), // .HS
	.vga_VS (VGA_VS), // .VS
	.vga_BLANK (VGA_BLANK_N), // .BLANK
	.vga_SYNC (VGA_SYNC_N), // .SYNC
	.vga_R (VGA_R), // .R
	.vga_G (VGA_G), // .G
	.vga_B (VGA_B), // .B
	.sram_DQ (SRAM_DQ), // sram.DQ
	.sram_ADDR (SRAM_ADDR), // .ADDR
	.sram_LB_N (SRAM_LB_N),
	.sram_UB_N (SRAM_UB_N), // .UB_N
	.sram_CE_N (SRAM_CE_N), // .CE_N
	.sram_OE_N (SRAM_OE_N), // .OE_N
	.sram_WE_N (SRAM_WE_N) 
	);
	endmodule