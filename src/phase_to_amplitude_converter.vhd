-- ==================================================
-- File: phase_to_amplitude_converter.vhd
-- Author: Craig Cochrane
-- Date: October 2024
-- --------------------------------------------------
-- MAP THE PHASE FROM THE PHASE ACCUMULATOR TO A SINE WAVE OUTPUT VALUE
--
-- Wraps the lookup tables and interpolator to output a 16-bit sine wave amplitude value from a 32-bit phase input
-- The sine and gradient ROMs are addressed with the top 10 bits of the phase value
-- The next 16 bits are used as the interpolation address
-- The final 6 bits are truncated
-- ==================================================
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity PHASE_TO_AMPLITUDE_CONVERTER is

port(
	CLK : in std_logic;
	RST : in std_logic;
	PHASE_IN : in std_logic_vector(31 downto 0);
	AMPLITUDE_OUT : out std_logic_vector(15 downto 0)
);

end entity PHASE_TO_AMPLITUDE_CONVERTER;

architecture RTL of PHASE_TO_AMPLITUDE_CONVERTER is

	signal INITIAL_POINT : std_logic_vector(15 downto 0); -- the output of the sine ROM
	signal GRADIENT : std_logic_vector(15 downto 0); -- the output of the gradient ROM

begin

	-- --------------------------------------------------
	-- INSTANTIATE THE SINE LOOKUP ROM
	-- --------------------------------------------------
	SINE_LOOKUP : entity work.SINE_ROM
	port map(
		CLK => CLK,
		RST => RST,
		ADDR_IN => PHASE_IN(31 downto 22),
		DATA_OUT => INITIAL_POINT
	);
	
	-- --------------------------------------------------
	-- INSTANTIATE THE GRADIENT LOOKUP ROM
	-- --------------------------------------------------
	GRADIENT_LOOKUP : entity work.GRADIENT_ROM
	port map(
		CLK => CLK,
		RST => RST,
		ADDR_IN => PHASE_IN(31 downto 22),
		DATA_OUT => GRADIENT
	);

	-- --------------------------------------------------
	-- INSTANTIATE THE INTERPOLATOR
	--
	-- The output of this is the final output value
	-- --------------------------------------------------
	INTERPOLATION : entity work.INTERPOLATOR
	port map(
	CLK => CLK,
	RST => RST,

	POINT_IN => INITIAL_POINT,
	GRADIENT_IN => GRADIENT,
	ADDR_IN => PHASE_IN(21 downto 6),

	VALUE_OUT => AMPLITUDE_OUT
	);

end architecture;