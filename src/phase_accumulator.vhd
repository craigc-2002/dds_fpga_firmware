-- ==================================================
-- File: phase_accumulator.vhd
-- Author: Craig Cochrane
-- Date: October 2025
-- --------------------------------------------------
-- DDS PHASE ACCUMULATOR
--
-- Defines the DDS phase accumulator entity 
-- On each clock cycle the phase increment word is added to the value in the accumulator
-- ==================================================

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity PHASE_ACCUMULATOR is
  generic
  (
    BIT_WIDTH : integer range 0 to 127
  );
  port
  (
    CLK : in std_logic;
    RST : in std_logic;

    PHASE_INCREMENT_WORD_IN : in std_logic_vector(BIT_WIDTH - 1 downto 0);
    PHASE_OUT               : out std_logic_vector(BIT_WIDTH - 1 downto 0)
  );
end entity PHASE_ACCUMULATOR;

architecture RTL of PHASE_ACCUMULATOR is

  signal PHASE_REGISTER : unsigned(BIT_WIDTH - 1 downto 0) := (others => '0');

begin

  PHASE_INCREMENT_PROC : process (CLK, RST) is
  begin
    if RST = '1' then
      PHASE_REGISTER <= (others => '0');
    elsif rising_edge(CLK) then
      PHASE_REGISTER <= PHASE_REGISTER + unsigned(PHASE_INCREMENT_WORD_IN);
    end if;
  end process PHASE_INCREMENT_PROC;

  PHASE_OUT <= std_logic_vector(PHASE_REGISTER);
  
 end architecture;
  