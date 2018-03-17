#!/usr/bin/perl

use Getopt::Std;
use Nmap::Parser;
use Date::Manip;

getopt("hi:o:");

$usage = "$0 -i input.xml -o output.csv";

if ($opt_h) {
        print "$usage\n";
};

if (!$opt_i || !$opt_o) { 
        print "$usage\n"; 
} else {
        my $np = new Nmap::Parser;
        $np->parsefile("$opt_i");

        # Start writing to results to the outputfile
        open (OUT,'>>'.$opt_o) || die "Could not open output file: $opt_o\n!";

        $si = $np->get_session();

        print   OUT "############\nNmap Version: ".$si->nmap_version()."\n",
                'Command Line: '.$si->scan_args()."\n";
        print OUT "Scan Date: ". $si->start_str()."\n";
        print OUT 'Total Time: '.($si->finish_time() - $si->start_time())." seconds\n##########\n";
		
		print OUT "addr;hostname;status;tcp open;udp open;extraports;extraportsstate;osmatch\n"; 
		for my $host ($np->all_hosts()) {
			my $tcp_ports = 0;
			my $udp_ports = 0;
			for my $port ($host->tcp_ports()) { $tcp_ports++ }
			for my $port ($host->udp_ports()) { $udp_ports++ }
			print OUT $host->addr().';'.
				$host->hostname().';'.
				$host->status().';'.
				$tcp_ports.';'.
				$udp_ports.';'.
				$host->extraports_count().';'.
				$host->extraports_state().';'.
				$host->os_sig->name."\n";
		}
		print OUT "##########\n";
		
        print OUT "addr;hostname;portnum;state;proto;name;product;version;extrainfo;extraports (count);osmatch\n"; 
        for my $host ($np->all_hosts()) {
                for my $port ($host->tcp_ports()) {
                        $sv = $host->tcp_service($port);

                        my $product = '';
                        my $version = '';               
                        my $extra = '';
                        my $osmatch = '';
                        my $extraports = '';
        
                        $product = $sv->product(); $product =~ s/\;/\,/g;
                        $version = $sv->version(); $version =~ s/\;/\,/g;
                $extra = $sv->extrainfo(); $extra =~ s/\;/\,/g;
                $osmatch = $host->os_sig->name; $osmatch =~ s/\;/\,/g;
                        $extraports = $host->extraports_state . " (" . $host->extraports_count() . ')';

                        print OUT $host->ipv4_addr().';';
                        print OUT $host->hostname().';';
                        print OUT $port.';'.
                        $host->tcp_port_state($port).';'.
                        'tcp;'.
                        $sv->name().';'.
                        $product.';'.
                        $version.';'.
                        $extra.';'.
                                $extraports.';'.
                        $osmatch."\n";
                }
                for my $port ($host->udp_ports()) {
                        $sv = $host->udp_service($port);

                        my $product = '';
                        my $version = '';               
                        my $extra = '';
                        my $osmatch = '';
                        my $extraports = '';

        
                        $product = $sv->product(); $product =~ s/\;/\,/g;
                        $version = $sv->version(); $version =~ s/\;/\,/g;
                $extra = $sv->extrainfo(); $extra =~ s/\;/\,/g;
                $osmatch = $host->os_sig->name; $osmatch =~ s/\;/\,/g;
                        $extraports = $host->extraports_state . " (" . $host->extraports_count() . ')';

                print OUT $host->ipv4_addr().';';
                        print OUT $host->hostname().';';
                        print OUT $port.';'.
                        $host->udp_port_state($port).';'.
                        'udp;'.
                        $sv->name().';'.
                        $product.';'.
                        $version.';'.
                        $extra.';'.
                                $extraports.';'.
                        $osmatch."\n";
                }
        }

}

