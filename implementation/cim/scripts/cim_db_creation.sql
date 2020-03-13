SET client_encoding = 'UTF8';

DROP DATABASE cim_operating_systems;

CREATE DATABASE cim_operating_systems;

\connect cim_operating_systems;

/*********** DATACENTERS ***********/

/*********** NETWORK ***********/

/*********** COMPUTE ***********/

/*********** STORAGE ***********/

/*********** OPERATING SYSTEMS ***********/

/* DATA TYPES */

CREATE TYPE public.operationalstatus AS ENUM (
	'Unknown', 
	'Other', 
	'OK', 
	'Degraded', 
	'Stressed', 
	'Predictive Failure', 
	'Error', 
	'Non-Recoverable Error', 
	'Starting', 
	'Stopping', 
	'Stopped', 
	'In Service', 
	'No Contact', 
	'Lost Communication', 
	'Aborted', 
	'Dormant', 
	'Supporting Entity in Error', 
	'Completed', 'Power Mode', 
	'Relocating', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.healthstate AS ENUM (
	'Unknown', 
	'OK', 
	'Degraded/Warning', 
	'Minor failure', 
	'Major failure', 
	'Critical failure', 
	'Non-recoverable error', 
	'DMTF Reserved', 
	'Vendor Specific'
);

CREATE TYPE public.primarystatus AS ENUM (
	'Unknown', 
	'OK', 
	'Degraded', 
	'Error', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.detailedstatus AS ENUM (
	'Not Available', 
	'No Additional Information', 
	'Stressed', 
	'Predictive Failure', 
	'Non-Recoverable Error', 
	'Supporting Entity in Error', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.operatingstatus AS ENUM (
	'Unknown', 
	'Not Available', 
	'Servicing', 
	'Starting', 
	'Stopping', 
	'Stopped', 
	'Aborted', 
	'Dormant', 
	'Completed', 
	'Migrating', 
	'Emigrating', 
	'Immigrating', 
	'Snapshotting', 
	'Shutting Down', 
	'In Test', 
	'Transitioning', 
	'In Service', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.communicationstatus AS ENUM (
	'Unknown', 
	'Not Available', 
	'Communication OK', 
	'Lost Communication', 
	'No Contact', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.enabledstate AS ENUM (
	'Unknown', 
	'Other', 
	'Enabled', 
	'Disabled', 
	'Shutting Down', 
	'Not Applicable', 
	'Enabled but Offline', 
	'In Test', 
	'Deferred', 
	'Quiesce', 
	'Starting', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.requestedstate AS ENUM (
	'Unknown', 
	'Enabled', 
	'Disabled', 
	'Shut Down', 
	'No Change', 
	'Offline', 
	'Test', 
	'Deferred', 
	'Quiesce', 
	'Reboot', 
	'Reset', 
	'Not Applicable', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.enableddefault AS ENUM (
	'Enabled', 
	'Disabled', 
	'Not Applicable', 
	'Enabled but Offline', 
	'No Default', 
	'Quiesce', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.transitioningtostate AS ENUM (
	'Unknown', 
	'Enabled', 
	'Disabled', 
	'Shut Down', 
	'No Change', 
	'Offline', 
	'Test', 
	'Defer', 
	'Quiesce', 
	'Reboot', 
	'Reset', 
	'Not Applicable', 
	'DMTF Reserved'
);

CREATE TYPE public.availablerequestedstates AS ENUM (
	'Enabled', 
	'Disabled', 
	'Shut Down', 
	'Offline', 
	'Test', 
	'Defer', 
	'Quiesce', 
	'Reboot', 
	'Reset', 
	'DMTF Reserved'
);

CREATE TYPE public.codeset AS ENUM (
	'Unknown', 
	'Other', 
	'ASCII', 
	'Unicode', 
	'ISO2022', 
	'ISO8859', 
	'Extended UNIX Code', 
	'UTF-8', 
	'UCS-2'
);

CREATE TYPE public.persistencetype AS ENUM (
	'Unknown', 
	'Other', 
	'Persistent', 
	'Temporary', 
	'External'
);

CREATE TYPE public.isfixedsize AS ENUM (
	'Not Specified', 
	'Fixed Size', 
	'Not Fixed Size'
);

CREATE TYPE public.ostype AS ENUM (
	'Unknown', 
	'Other', 
	'MACOS', 
	'ATTUNIX', 
	'DGUX', 
	'DECNT', 
	'Tru64 UNIX', 
	'OpenVMS', 
	'HPUX', 
	'AIX', 
	'MVS', 
	'OS400', 
	'OS/2', 
	'JavaVM', 
	'MSDOS', 
	'WIN3x', 
	'WIN95', 
	'WIN98', 
	'WINNT', 
	'WINCE', 
	'NCR3000', 
	'NetWare', 
	'OSF', 
	'DC/OS', 
	'Reliant UNIX', 
	'SCO UnixWare', 
	'SCO OpenServer', 
	'Sequent', 
	'IRIX', 
	'Solaris', 
	'SunOS', 
	'U6000', 
	'ASERIES', 
	'HP NonStop OS', 
	'HP NonStop OSS', 
	'BS2000', 
	'LINUX', 
	'Lynx', 
	'XENIX', 
	'VM', 
	'Interactive UNIX', 
	'BSDUNIX', 
	'FreeBSD', 
	'NetBSD', 
	'GNU Hurd', 
	'OS9', 
	'MACH Kernel', 
	'Inferno', 
	'QNX', 
	'EPOC', 
	'IxWorks', 
	'VxWorks', 
	'MiNT', 
	'BeOS', 
	'HP MPE', 
	'NextStep', 
	'PalmPilot', 
	'Rhapsody', 
	'Windows 2000', 
	'Dedicated', 
	'OS/390', 
	'VSE', 
	'TPF', 
	'Windows (R) Me', 
	'Caldera Open UNIX', 
	'OpenBSD', 
	'Not Applicable', 
	'Windows XP', 
	'z/OS', 
	'Microsoft Windows Server 2003', 
	'Microsoft Windows Server 2003 64-Bit', 
	'Windows XP 64-Bit', 
	'Windows XP Embedded', 
	'Windows Vista', 
	'Windows Vista 64-Bit', 
	'Windows Embedded for Point of Service', 
	'Microsoft Windows Server 2008', 
	'Microsoft Windows Server 2008 64-Bit', 
	'FreeBSD 64-Bit', 
	'RedHat Enterprise Linux', 
	'RedHat Enterprise Linux 64-Bit', 
	'Solaris 64-Bit', 
	'SUSE', 
	'SUSE 64-Bit', 
	'SLES', 
	'SLES 64-Bit', 
	'Novell OES', 
	'Novell Linux Desktop', 
	'Sun Java Desktop System', 
	'Mandriva', 
	'Mandriva 64-Bit', 
	'TurboLinux', 
	'TurboLinux 64-Bit', 
	'Ubuntu', 
	'Ubuntu 64-Bit', 
	'Debian', 
	'Debian 64-Bit', 
	'Linux 2.4.x', 
	'Linux 2.4.x 64-Bit', 
	'Linux 2.6.x', 
	'Linux 2.6.x 64-Bit', 
	'Linux 64-Bit', 
	'Other 64-Bit', 
	'Microsoft Windows Server 2008 R2', 
	'VMware ESXi', 
	'Microsoft Windows 7', 
	'CentOS 32-bit', 
	'CentOS 64-bit', 
	'Oracle Linux 32-bit', 
	'Oracle Linux 64-bit', 
	'eComStation 32-bitx', 
	'Microsoft Windows Server 2011', 
	'Microsoft Windows Server 2012', 
	'Microsoft Windows 8', 
	'Microsoft Windows 8 64-bit', 
	'Microsoft Windows Server 2012 R2', 
	'Microsoft Windows Server 2016', 
	'Microsoft Windows 8.1', 
	'Microsoft Windows 8.1 64-bit', 
	'Microsoft Windows 10', 
	'Microsoft Windows 10 64-bit'
);

CREATE TYPE public.nameformat AS ENUM (
	'Other', 
	'IP', 
	'Dial', 
	'HID', 
	'NWA', 
	'HWA', 
	'X25', 
	'ISDN', 
	'IPX', 
	'DCC', 
	'ICD', 
	'E.164', 
	'SNA', 
	'OID/OSI', 
	'WWN', 
	'NAA', 
	'UUID'
);

CREATE TYPE public.dedicated AS ENUM (
	'Not Dedicated', 
	'Unknown', 
	'Other', 
	'Storage', 
	'Router', 
	'Switch', 
	'Layer 3 Switch', 
	'Central Office Switch', 
	'Hub', 
	'Access Server', 
	'Firewall', 
	'Print', 
	'I/O', 
	'Web Caching', 
	'Management', 
	'Block Server', 
	'File Server', 
	'Mobile User Device', 
	'Repeater', 
	'Bridge/Extender', 
	'Gateway', 
	'Storage Virtualizer', 
	'Media Library', 
	'ExtenderNode', 
	'NAS Head', 
	'Self-contained NAS', 
	'UPS', 
	'IP Phone', 
	'Management Controller', 
	'Chassis Manager', 
	'Host-based RAID controller', 
	'Storage Device Enclosure', 
	'Desktop', 
	'Laptop', 
	'Virtual Tape Library', 
	'Virtual Library System', 
	'Network PC/Thin Client', 
	'FC Switch', 
	'Ethernet Switch', 
	'Server', 
	'Blade', 
	'Partitioned Library System', 
	'Unallocated Partition', 
	'Partition', 
	'DMTF Reserved', 
	'Vendor Reserved'
);

CREATE TYPE public.resetcapability AS ENUM (
	'Other', 
	'Unknown', 
	'Disabled', 
	'Enabled', 
	'Not Implemented'
);

/* CLASSES */

CREATE TABLE public.managedelement (
	id SERIAL PRIMARY KEY,
	caption character varying(255),
	description character varying(255),
	elementname character varying(255),
	instanceid character varying(255),
	generation numeric(64)
);

CREATE TABLE public.managedsystemelement(
	id SERIAL PRIMARY KEY,
	installdate timestamp without time zone,
	name character varying(255),
	operationalstatus public.operationalstatus[],
	healthstate public.healthstate,
	primarystatus public.primarystatus,
	detailedstatus public.detailedstatus,
	operatingstatus public.operatingstatus,
	communicationstatus public.communicationstatus,
	managedelementid SERIAL,
	FOREIGN KEY (managedelementid) REFERENCES managedelement (id)
);

CREATE TABLE public.logicalelement (
	id SERIAL PRIMARY KEY,
	managedsystemelementid SERIAL,
	FOREIGN KEY (managedsystemelementid) REFERENCES managedsystemelement (id)
);

CREATE TABLE public.enabledlogicalelement (
	id SERIAL PRIMARY KEY,
	enabledstate public.enabledstate,
	otherenabledstate character varying(255),
	requestedstate public.requestedstate,
	enableddefault public.enableddefault,
	timeoflaststatechange timestamp without time zone,
	transitioningtostate public.transitioningtostate,
 	availablerequestedstates public.availablerequestedstates[],
	logicalelementid SERIAL,
	FOREIGN KEY (logicalelementid) REFERENCES logicalelement (id)
);

CREATE TABLE public.alocatedlogicalelement (
	id SERIAL PRIMARY KEY,
	allocationstate character varying(255),
	enabledlogicalelementid SERIAL,
	FOREIGN KEY (enabledlogicalelementid) REFERENCES enabledlogicalelement (id)
);

CREATE TABLE public.system (
	id SERIAL PRIMARY KEY,
	creationclassname character varying(255),
	name character varying(255),
	nameformat character varying(255),
	primaryownername character varying(255), 
	primaryownercontact character varying(255), 
	roles text[],
	otheridentifyinginfo text[],
	identifyingdescriptions text[],
	alocatedlogicalelementid SERIAL,
	FOREIGN KEY (alocatedlogicalelementid) REFERENCES alocatedlogicalelement (id)
);

CREATE TABLE public.computersystem (
	id SERIAL PRIMARY KEY,
	nameformat public.nameformat,
	dedicated public.dedicated,
	otherdedicateddescriptions text[],
	resetcapability public.resetcapability,
	systemid SERIAL,
	FOREIGN KEY (systemid) REFERENCES system (id)
);

CREATE TABLE public.filesystem (
	id SERIAL PRIMARY KEY,
	creationclassname character varying(255),
	name character varying(255),
	root character varying(255),
	blocksize numeric(64),
	filesystemsize numeric(64),
	availablespace numeric(64),
	readonly boolean,
	encryptionmethod character varying(255),
	compressionmethod character varying(255),
	casesensitive boolean,
	casepreserved boolean,
	codeset public.codeset[],
	maxfilenamelength numeric(32),
	clustersize numeric(32),
	filesystemtype character varying(255),
	persistencetype public.persistencetype,
	otherpersistencetype character varying(255),
	numberoffiles numeric(64),
	isfixedsize public.isfixedsize,
	resizeincrement numeric(16),
	enabledlogicalelementid SERIAL,
	FOREIGN KEY (enabledlogicalelementid) REFERENCES enabledlogicalelement (id)
);

CREATE TABLE public.operatingsystem (
	id SERIAL PRIMARY KEY,
	creationclassname character varying(255),
	name character varying(255),
	ostype public.ostype,
	othertypedescription character varying(255),
	version character varying(255),
	lastbootuptime timestamp without time zone,
	localdatetime timestamp without time zone,
	currenttimezone numeric(16),
	numberoflicensedusers numeric(32),
	numberofusers numeric(32),
	numberofprocesses numeric(32),
	maxnumberofprocesses numeric(32),
	totalswapspacesize numeric(64),
	totalvirtualmemorysize numeric(64),
	freevirtualmemory numeric(64),
	freephysicalmemory numeric(64),
	totalvisiblememorysize numeric(64),
	sizestoredinpagingfiles numeric(64),
	freespaceinpagingfiles numeric(64),
	maxprocessmemorysize numeric(64),
	distributed boolean,
	maxprocessesperuser numeric(32),
	manufacturer character varying(255),
	family character varying(255),
	osclassification character varying(255),
	enabledlogicalelementid SERIAL,
	FOREIGN KEY (enabledlogicalelementid) REFERENCES enabledlogicalelement (id)
);

/* ASSOCIATIONS */

CREATE TABLE public.bootosfromfs (
	filesystemid SERIAL,
	operatingsystemid SERIAL,
	PRIMARY KEY (filesystemid, operatingsystemid),
	FOREIGN KEY (filesystemid) REFERENCES filesystem (id),
	FOREIGN KEY (operatingsystemid) REFERENCES operatingsystem (id)
);

CREATE TABLE public.runningos (
	computersystemid SERIAL,
	operatingsystemid SERIAL,
	PRIMARY KEY (computersystemid, operatingsystemid),
	FOREIGN KEY (computersystemid) REFERENCES computersystem (id),
	FOREIGN KEY (operatingsystemid) REFERENCES operatingsystem (id)
);

CREATE TABLE public.installedos (
	computersystemid SERIAL,
	operatingsystemid SERIAL,
	primaryos boolean,
	PRIMARY KEY (computersystemid, operatingsystemid),
	FOREIGN KEY (computersystemid) REFERENCES computersystem (id),
	FOREIGN KEY (operatingsystemid) REFERENCES operatingsystem (id)
);

/*********** END USER DEVICES ***********/







