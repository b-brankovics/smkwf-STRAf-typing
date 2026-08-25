#!/usr/bin/env perl
use strict;
use warnings;

my ( $fasta, $tsv, $sample ) = @ARGV;

open my $in, '<', $tsv or die "Could not open $tsv: $!";

my %loci;
while (<$in>) {
    s/\R//g;
    my ( $locus, $flanking, $len, $repeat ) = split /\t/;
    next if $locus eq "locus";
    $loci{$locus} = $repeat;
}

# Hash to store the sequences: key (id and defintion) and value (sequence)
my %fas_data;

# Array to store the order of the sequences
my @ids;

&read_fasta( \%fas_data, \@ids, $fasta );

print join( "\t",
    "sample",     "locus",        "count",
    "upstream",   "downstream",   "Repeat_seq",
    "Bad_repeat", "upstream_seq", "downstream_seq" )
  . "\n";
for my $locus ( sort keys %loci ) {
    my $repeat = $loci{$locus};
    &screen( $locus, $repeat, \%fas_data, \@ids );
}

sub screen {
    my ( $locus, $repeat, $fasta_hash, $ids_array ) = @_;
    my @ids      = @{$ids_array};
    my %fas_data = %{$fasta_hash};

    my $n = length $repeat;

    # There can be imperfect repeats near the ends of the repeat region,
    # so we allow for 1 imperfect repeat at positions 2 or 3 from the end.
    my $regex0 = "^" . "(.*?)"
      . "(?:${repeat})+(?:.{$n})?(?:${repeat})+"    # This maybe too short
      . "(.*?)" . '$';
    my $regex = "^" . "(.*?)"
      . "((?:${repeat}){1,2}.{$n}(?:${repeat}){2,}.{$n}(?:${repeat}){1,2})"
      . "(.*?)" . '$';

    # The above regex fails if repeat count is less than 6
    my $regex2 = "^" . "(.*?)"
      . "((?:${repeat}){1,2}.{$n}(?:${repeat})+.{$n}(?:${repeat}){1,2})"
      . "(.*?)" . '$';

    # Skip imperfect repeats for short repeat regions
    my $regex3 = "^" . "(.*?)" . "((?:${repeat}){2,})" . "(.*?)" . '$';

    my $hit;
    for (@ids) {
        next unless /\b$locus\b/;
        next if length( $fas_data{$_} ) > 2000;

        # my ($id) = split/\|/;
        $fas_data{$_} = uc $fas_data{$_};

        my ( $pre, $target, $post );
        for my $regex ( $regex0, $regex, $regex2, $regex3 ) {
            if ( $fas_data{$_} =~ /$regex/ && length $2 > $target ) {
                ( $pre, $target, $post ) = ( $1, $2, $3 );
            }
        }
        if ($target) {
            $hit++;
            my @rep   = ( $target =~ m/.{$n}/g );
            my $count = scalar @rep;
            my @bad;
            my $i;
            for (@rep) {
                $i++;
                push @bad, $i unless /${repeat}/;
            }
            my $note = "";
            for (@bad) {
                $note .= " " if $note;
                if ( $count - $_ < $_ ) {
                    $note .= "-" . ( $count - $_ + 1 );
                }
                else {
                    $note .= "$_";
                }
            }

# print join("\t", "sample", "locus", "count", "upstream", "downstream", "Repeat_seq", "Bad_repeat"). "\n";
            print join( "\t",
                $sample, $locus, $count, ( map { length $_ } ( $pre, $post ) ),
                $target, $note,  $pre, $post )
              . "\n";
        }
    }
    unless ($hit) {
        print join( "\t", $sample, $locus, "NA", "NA", "NA", "NA", "NA" )
          . "\n";
    }
}

sub read_fasta {

    # Convert FASTA string into a hash with IDs for keys and sequences
    #  as values and stores the original order in an array
    # This subroutine requires three arguments:
    #	1) filehandle for the FASTA file
    #	2) a hash reference to store the sequences in
    #	3) an array reference to store the IDs in the same
    #          order as the original file
    # If an ID line is present multiple times then a warning is printed
    #  to STDERR
    my ( $hash, $list, $file ) = @_;

    # Use STDIN if file is '-'
    $file = undef if $file && $file eq '-';
    my $in;
    if ( $file && -e $file ) {
        open $in, '<', $file || die $!;
    }
    else {
        $in = *STDIN;
    }

    # Store the sequence id
    my $seq_id;
    for (<$in>) {

        # Remove line endings
        s/\R//g;

        # Skip empty lines
        next if /^\s*$/;

        # Check wheter it is an id line
        if (/>(.*)/) {

            # Save the id and the definition and store it in the array
            $seq_id = $1;
            print {*STDERR}
              "WARNING: <$seq_id> is present in multiple copies\n"
              if $hash->{$seq_id};
            push @$list, $seq_id;
        }
        else {
            # If there was no id lines before this then throw an error
            unless ( defined $seq_id ) {
                print "Format error in FASTA file! Check the file!\n";
                last;
            }

            # Remove white space
            s/\s+//g;

            # Add to the sequence
            $hash->{$seq_id} .= $_;
        }
    }
    close $in;
}

