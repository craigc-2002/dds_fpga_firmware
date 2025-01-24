# VHDL Lookup Table Generator
# Craig Cochrane, 2024
#
# Generate VHDL file to implement a lookup table using case statement
# Will be inferred as ROM and implemented using BRAM in iCE40
#
# TODO: Allow lookup table values to be signed

import datetime
import math

class VHDLLookupGenerator:
    def __init__(self, table_data, entity_name, output_filename=None, data_bits=16, default_value=0, data_type="unsigned"):

        self.lookup_table = table_data
        self.entity_name = entity_name

        if not(output_filename):
            self.output_filename = entity_name + ".vhd"
        else:
            self.output_filename = output_filename
    
        self.table_length = len(self.lookup_table)
        self.address_bits = math.ceil(math.log2(self.table_length))
        self.data_bits = data_bits

        self.default_value = default_value # the value given in the "others" case
        self.data_type = data_type # signed or unsigned output values

    def generate_table(self):

        output_file = open(self.output_filename, "w")

        print(f"""-- ==================================================
-- File: {self.output_filename}
-- --------------------------------------------------
-- Autogenerated by python script
-- Date: {datetime.date.today()}
-- --------------------------------------------------
-- Lookup table length: {self.table_length}
-- Number of address bits: {self.address_bits}
-- Number of data bits: {self.data_bits}
-- ==================================================
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity {self.entity_name} is
port
(
CLK      : in  std_logic;
RST      : in  std_logic;
ADDR_IN  : in  std_logic_vector({self.address_bits-1} downto 0);
DATA_OUT : out std_logic_vector({self.data_bits-1} downto 0)
);
end entity {self.entity_name};

architecture RTL of {self.entity_name} is	

signal ADDR : std_logic_vector({self.address_bits-1} downto 0) := (others => '0');
signal DATA : {self.data_type}({self.data_bits-1} downto 0) := (others => '0');

-- tell the synthesis engine to use BRAM for inferred ROMs
attribute syn_romstyle : string;
attribute syn_romstyle of RTL : architecture is "block_rom";						 

begin

-- --------------------------------------------------
-- PROCESS TO READ FROM INFERRED ROM
-- --------------------------------------------------
ROM_PROC : process(CLK) is
begin

if rising_edge(CLK) then
case ADDR is""",
        file=output_file)

        for i, value in enumerate(self.lookup_table):
            print(f"\twhen \"{i:0{self.address_bits}b}\" => DATA <= to_{self.data_type}({value}, {self.data_bits});", file=output_file)
            
        print(f"""when others  => DATA <= to_unsigned({self.default_value}, {self.data_bits});
end case;
end if;
end process;

-- --------------------------------------------------
-- PROCESS TO REGISTER ADDRESS INPUT AND DATA OUTPUT ON CLOCK EDGE
-- --------------------------------------------------
DATA_PROC : process(RST, CLK) is
begin

if RST='1' then
    DATA_OUT <= (others => '0');
    ADDR <= (others => '0');
elsif rising_edge(CLK) then
    DATA_OUT <= std_logic_vector(DATA);
    ADDR <= ADDR_IN;
end if;

end process;
end architecture RTL;""",
        file=output_file)

        output_file.close()