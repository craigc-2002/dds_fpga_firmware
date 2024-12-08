-- ==================================================
-- File: interpolator.vhd
-- Author: Craig Cochrane
-- Date: October 2024
-- --------------------------------------------------
-- PERFORMS LINEAR INTERPOLATION BETWEEN TWO ADJACENT POINTS IN THE SINE ROM
--
-- Takes in the first point, gradient and interpolation address and outputs the interpolated value
-- All input values and the output value are 16-bit
-- 
-- Performing the addition and multiplication in seperate clocked processes pipelines these operations
-- which increases clock speed at the expense of a couple of clock cycles of latency
-- ==================================================
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity INTERPOLATOR is
  port
  (
    CLK : in std_logic; -- active high reset
    RST : in std_logic;

	POINT_IN : in std_logic_vector(15 downto 0);
	GRADIENT_IN : in std_logic_vector(15 downto 0);
	ADDR_IN : in std_logic_vector(15 downto 0);
	
	VALUE_OUT : out std_logic_vector(15 downto 0)
  );
end entity INTERPOLATOR;

architecture RTL of INTERPOLATOR is

	signal POINT        : signed   (16 downto 0)    := to_signed(0, 17);
	signal POINT_DELAY  : signed   (16 downto 0)    := to_signed(0, 17); -- point value delayed by 1 clock cycle
	signal GRADIENT     : signed   (15 downto 0)    := to_signed(0, 16);
	signal ADDR         : signed   (16 downto 0)    := to_signed(0, 17);
	signal MULT_RESULT  : signed   (32 downto 0)    := to_signed(0, 33);  -- full output of the gradient and address multiplier
	signal INTERP       : signed   (9 downto  0)    := to_signed(0, 10); -- the value added by the linear interpolation
	signal INTERP_POINT : signed   (16 downto 0)    := to_signed(0, 17); -- the point found by linear interpolation

begin

	-- --------------------------------------------------
	-- MULTIPLICATION_PROC
	-- --------------------------------------------------
	-- The gradient is multiplied by the phase address to find the value to be added by the interpolation.
	--
	-- Since the lower 6 bits of the phase address are truncated, the result has to be left shifted by 6 bits.
	-- The result also has to be right shifted by 29 bits due to the fact that the gradient value stored in the lookup table is
	-- shifted up by 29 bits to use the full resolution of a signed 16-bit fixed point representation
	--
	-- This means that only the top 10 bits of the multiplication result are needed (9 bits plus sign bit)
	-- --------------------------------------------------
	MULTIPLICATION_PROC : process(CLK, RST) is
	begin
	
		if rising_edge(CLK) then
			MULT_RESULT <= GRADIENT * ADDR;
		end if;
	
	end process;
	
	
	-- --------------------------------------------------
	-- ADD_PROC
	-- --------------------------------------------------
	-- add the interpolated value to the initial point
	-- --------------------------------------------------
	ADD_PROC: process(CLK, RST) is
	begin
	
		INTERP_POINT <= POINT_DELAY + INTERP;
	
	end process;
	
	
	
	-- --------------------------------------------------
	-- REGISTER_PROC
	-- --------------------------------------------------
	-- register the input values on the rising clock edge
	-- --------------------------------------------------
	REGISTER_PROC : process(CLK, RST) is
	begin
	
		if rising_edge(CLK) then
			POINT_DELAY <= POINT;
			POINT <= signed('0' & POINT_IN);
			GRADIENT <= signed(GRADIENT_IN);
			ADDR <= signed('0' & ADDR_IN);
		end if;
	
	end process;
	
	
	-- --------------------------------------------------
	-- ASYNCHRONOUS ASSIGNMENTS
	-- --------------------------------------------------
	INTERP <= MULT_RESULT(32 downto 23);
	VALUE_OUT <= std_logic_vector(INTERP_POINT(15 downto 0));

end architecture;