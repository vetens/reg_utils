library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package common_datatypes_pkg is

    type t_std_array is array(integer range <>) of std_logic; 
    type t_std32_array is array(integer range <>) of std_logic_vector(31 downto 0);
    type t_std24_array is array(integer range <>) of std_logic_vector(23 downto 0);
    type t_std16_array is array(integer range <>) of std_logic_vector(15 downto 0);
    type t_std14_array is array(integer range <>) of std_logic_vector(13 downto 0);
    type t_std10_array is array(integer range <>) of std_logic_vector(9 downto 0);
    type t_std8_array is array(integer range <>) of std_logic_vector(7 downto 0);
    type t_std4_array is array(integer range <>) of std_logic_vector(3 downto 0);
    type t_std3_array is array(integer range <>) of std_logic_vector(2 downto 0);
    type t_std2_array is array(integer range <>) of std_logic_vector(1 downto 0);
    type t_std176_array is array(integer range <>) of std_logic_vector(175 downto 0);
    	
end common_datatypes_pkg;
