# reg-utils
GENERAL DESCRIPTION NEEDED

The fw_modules directory includes the modules necessary for the generator to work correctly, as well as some handy utilities (optional).
For generator to work you should include these files in your project: fw_modules/ipbus_slave.vhd, fw_modules/pkg/*.vhd, fw_modules/utils/synchronizer.vhd
At the top level you will need to connect the physical register access port to the ipbus_slaves. If you're using AXI to communicate to the outside world, then you can use the included axi_ipbus_bridge module for that (note that you'll need to edit the ipb_addr_decode_EXAMPLE.vhd to match your project -- this file defines the number of ipbus slaves, and the routing to these slaves based on the address pattern -- this could also be automated later on).
If you already have a wishbone bus and want to fan it out to the different ipbus slaves, we also have a module for that (not yet commited, Andrew will commit that soon I believe).

Additionally in fw_modules/util you will find some generic useful firmware utilities like: counter, rate_counter, oneshot, oneshot_cross_domain, latch, pulse_extend, synchronizer. Refer to the description section in each of these files for more info.
