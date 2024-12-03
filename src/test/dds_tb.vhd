-- ==================================================
-- File: dds_tb.vhd
-- Author: Craig Cochrane
-- Date: October 2025
-- --------------------------------------------------
-- TEST BENCH FOR DDS TOP LEVEL
--
-- Top level test bench to verify the operation of the DDS firmware
-- ==================================================
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity DDS_TB is
end entity DDS_TB;

architecture TEST of DDS_TB is

	-- Timing constants
	constant CLK_PERIOD : time := 10ns; -- 100 MHz clock
	constant RST_PERIOD : time := 8ns;

	-- Signals to connect to the UUT
	signal CLK  : std_logic                    := '0';
	signal NRST  : std_logic                   := '0';
	signal LEDS : std_logic_vector(7 downto 0) := (others => '0'); 
	signal DAC_DATA : std_logic_vector(15 downto 0);
	signal DAC_CLK : std_logic;

	-- DDS Component
	component DDS_FPGA_TOP_LEVEL is
	port
	(
		CLK : in std_logic;
		NRST : in std_logic;

		DAC_CLK_OUT : out std_logic;
	    LED_OUT   : out std_logic_vector(7 downto 0);  -- outputs to the 8 LEDs on the Alchitry Cu board
		DAC_OUT   : out std_logic_vector(15 downto 0) -- outputs to the DAC parallel data outputs
	);
	end component DDS_FPGA_TOP_LEVEL;

	begin

	-- Unit Under Test
	UUT : DDS_FPGA_TOP_LEVEL
	port map
	(
	CLK     => CLK,
	NRST     => NRST,	   	
	DAC_CLK_OUT => DAC_CLK,
	LED_OUT => LEDS,
	DAC_OUT =>  DAC_DATA
	);

	-- Clock and Reset generation
	CLK <= not(CLK) after CLK_PERIOD/2;
	NRST <= '1' after RST_PERIOD;

end architecture TEST;
