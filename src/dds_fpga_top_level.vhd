-- ==================================================
-- File: dds_fpga_top_level.vhd
-- Author: Craig Cochrane
-- Date: November 2024
-- --------------------------------------------------
-- TOP LEVEL ENTITY FOR DDS FPGA
--
-- Initial test setup where the phase accumulator value is converted to a sine value simply using a lookup table
-- The top 8 bits of the sine value are sent to the LEDs on the iCE40 dev board to allow the wave to be visualised
-- The full 16 bits are output to the DAC
-- A DAC clock is generated with a PLL
-- The phase accumulator is set up with a constant phase increment value to give a 1 Hz output
--
-- DAC clock is created by a PLL to set it 90 degrees out of phase from the FPGA clock
-- This ensures that the DAC clock and data timing requirements from the datasheet are met:
-- 		Setup time: 0.4ns
-- 		Hold time:  1.25ns
-- 		Propagation delay time: 1.8ns (time between falling CLK edge and output change)
--		There is a 3.5 clock-cycle latency between CLKP/CLKN transitioning high/low and IOUTP/IOUTN
-- ==================================================

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity DDS_FPGA_TOP_LEVEL is
  port
  (
    CLK  : in std_logic;
    NRST : in std_logic;
	
	DAC_CLK_OUT : out std_logic;
    LED_OUT   : out std_logic_vector(7 downto 0);  -- outputs to the 8 LEDs on the Alchitry Cu board
	DAC_OUT   : out std_logic_vector(15 downto 0) -- outputs to the DAC parallel data outputs
  );
end entity;

architecture RTL of DDS_FPGA_TOP_LEVEL is

	signal RST : std_logic;
	signal DAC_CLK : std_logic;
	signal PHASE : std_logic_vector(31 downto 0) := (others=>'0');
	signal DATA  : std_logic_vector(15 downto 0) := (others=>'0');  
	
	-- hardcoded phase increment value of 43 to give 1 Hz sine wave output with 100 MHz clock input
	constant PHASE_INCREMENT : unsigned(31 downto 0) := to_unsigned(43, 32);
  
begin

	-- --------------------------------------------------
	-- INSTANTIATE THE PHASE ACCUMULATOR
	-- --------------------------------------------------
	PHASE_ACC : entity work.PHASE_ACCUMULATOR
	generic map(
		BIT_WIDTH => 32
	)
	port map(
		CLK => CLK,
		RST => RST,
		PHASE_INCREMENT_WORD_IN => std_logic_vector(PHASE_INCREMENT), 
		PHASE_OUT => PHASE
	);
	
	-- --------------------------------------------------
	-- INSTANTIATE THE SINE WAVE LOOKUP TABLE
	-- --------------------------------------------------
	SINE_LOOKUP : entity work.SINE_ROM
	port map(
		CLK => CLK,
		RST => RST,
		ADDR_IN => PHASE(31 downto 22),
		DATA_OUT => DATA
	);
	
	-- --------------------------------------------------
	-- INSTANTIATE PLL FOR DAC CLOCK
	-- 
	-- Reference clock: 100 MHz system clock
	-- Output clock: 100 MHz clock with 90 degree phase shift
	-- --------------------------------------------------
	DAC_PLL_INST : entity work.DDS_FPGA_TOP_LEVEL_pll
	port map
	(
	REFERENCECLK => CLK,
	RESET        => '1', -- active low reset
	PLLOUTCORE   => open,
	PLLOUTGLOBAL => DAC_CLK
	);
	
	-- --------------------------------------------------
	-- OUTOUT AMPLITUDE TO DAC
	-- Also output top 8 bits to LEDs
	-- --------------------------------------------------
	DAC_OUT <= DATA when RST = '0' else X"0000";
	LED_OUT <= DATA(15 downto 8) when RST = '0' else X"00";
	
	-- --------------------------------------------------
	-- ASYCHRONOUS ASSIGNMENTS
	-- --------------------------------------------------
	RST <= not(NRST);
	DAC_CLK_OUT <= DAC_CLK;

end RTL;