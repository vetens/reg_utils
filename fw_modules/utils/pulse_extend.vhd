------------------------------------------------------------------------------------------------------------------------------------------------------
-- Company: TAMU
-- Engineer: Evaldas Juska (evaldas.juska@cern.ch, evka85@gmail.com)
-- 
-- Create Date:    23:40 2016-12-18
-- Module Name:    pulse_extend 
-- Description:    after pulse_i transitions from high to low, the pulse_o signal will be held high for DELAY_CNT_LENGTH clock cycles and then go low
------------------------------------------------------------------------------------------------------------------------------------------------------


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pulse_extend is
  generic (
    DELAY_CNT_LENGTH : integer := 8
    );
  port (
    clk_i          : in  std_logic;
    rst_i          : in  std_logic;
    pulse_length_i : in  std_logic_vector (DELAY_CNT_LENGTH-1 downto 0);
    pulse_i        : in  std_logic;
    pulse_o        : out std_logic
    );
end pulse_extend;

architecture pulse_extend_arch of pulse_extend is

  signal s_count_down_cnt : unsigned(DELAY_CNT_LENGTH-1 downto 0);

begin

  process(clk_i) is
  begin
    if rising_edge(clk_i) then
      if rst_i = '1' then
        s_count_down_cnt <= to_unsigned(0, DELAY_CNT_LENGTH);
      elsif pulse_i = '1' then
        s_count_down_cnt <= unsigned(pulse_length_i);
      elsif s_count_down_cnt = to_unsigned(0, DELAY_CNT_LENGTH) then
        s_count_down_cnt <= to_unsigned(0, DELAY_CNT_LENGTH);
      else
        s_count_down_cnt <= s_count_down_cnt - 1;
      end if;
    end if;
  end process;

  process(clk_i) is
  begin
    if rising_edge(clk_i) then
      if s_count_down_cnt /= 0 then
        pulse_o <= '1';
      else
        pulse_o <= '0';
      end if;
    end if;
  end process;

end pulse_extend_arch;
