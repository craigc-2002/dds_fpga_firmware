-- ==================================================
-- File: phase_accumulator_tb.vhd
-- Author: Craig Cochrane
-- Date: October 2025
-- --------------------------------------------------
-- TEST BENCH FOR DDS PHASE ACCUMULATOR
--
-- Tests operation of the phase accumulator using a 4-bit accumulator so that simulation is not too long
-- The phase increment is set to 1 so that the accumulator goes through all output values
-- ==================================================

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity PHASE_ACCUMULATOR_TB is
end entity PHASE_ACCUMULATOR_TB;

architecture TEST of PHASE_ACCUMULATOR_TB is

  -- Timing constants
  constant CLK_PERIOD : time := 10ns;
  constant RST_PERIOD : time := 8ns;

  -- Test phase accumulator with 4 bits to demonstrate overflow behaviour quickly
  constant NUM_BITS : integer := 4;

  -- Signals to connect to the UUT
  signal CLK                  : std_logic                               := '0';
  signal RST                  : std_logic                               := '1';
  signal PHASE_INCREMENT_WORD : std_logic_vector(NUM_BITS - 1 downto 0) := (0 => '1', others => '0'); -- set phase increment to 1
  signal PHASE                : std_logic_vector(NUM_BITS - 1 downto 0) := (others => '0');

  -- Phase Accumulator Component
  component PHASE_ACCUMULATOR is
    generic
    (
      BIT_WIDTH : integer
    );
    port
    (
      CLK                     : in std_logic;
      RST                     : in std_logic;
      PHASE_INCREMENT_WORD_IN : in std_logic_vector(NUM_BITS - 1 downto 0);
      PHASE_OUT               : out std_logic_vector(NUM_BITS - 1 downto 0)
    );
  end component PHASE_ACCUMULATOR;

begin

  -- Unit Under Test
  UUT : PHASE_ACCUMULATOR
  generic
  map(
  BIT_WIDTH => NUM_BITS
  )
  port map
  (
    CLK                     => CLK,
    RST                     => RST,
    PHASE_INCREMENT_WORD_IN => PHASE_INCREMENT_WORD,
    PHASE_OUT               => PHASE
  );

  -- Clock and Reset generation
  CLK <= not(CLK) after CLK_PERIOD/2;
  RST <= '0' after RST_PERIOD;

end architecture TEST;