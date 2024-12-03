-- ==================================================
-- File: pll_mock.vhd
-- Author: Craig Cochrane
-- Date: December 2024
-- --------------------------------------------------
-- PLL MOCK
--
-- Basic entity with the same name and ports as the iCE40 PLL to allow the simulation to compile
-- Just passes the input clock through to the output, so the DAC clock output will not have the correct phase in simulation.
-- ==================================================
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity DDS_FPGA_TOP_LEVEL_pll is
port
(
REFERENCECLK : in std_logic;
RESET        : in std_logic;
PLLOUTCORE   : out std_logic;
PLLOUTGLOBAL : out std_logic
);

end entity;

architecture MOCK of DDS_FPGA_TOP_LEVEL_pll is

begin

PLLOUTGLOBAL <= REFERENCECLK;

end architecture;