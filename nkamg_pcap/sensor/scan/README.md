# Source code illustration

## scan.py module

This module is in charge of: 

1. getting args from CLS (function `get_args()`)
2. converting args to nmap command (function `get_cmd()`)
3. requiring `nmap_scan` module for executing command (function `scan()`)

## nmap_scan.py module

This module is in charge of:

1. executing nmap scan and putting the result in xml file (`_scan_with_xml_output()`)
2. extracting information that we need from xml file (`_extract_from_xml()`)
3. storing such information in the format of csv (`_store_as_csv()`)

- `_get_csv()` function includes the step of extraction and storage. It is also use for test.

## info_class.py module

In this module I defined some structure for storing specific information.
