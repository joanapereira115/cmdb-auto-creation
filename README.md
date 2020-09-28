# CMDB Automatic Creation

Computing infrastructure management is becoming more demanding and must increasingly comply with regulatory requirements.

To meet these requirements, a CMDB is essential. One of the challenges any team has to begin managing an existing infrastructure is building this CMDB.

So, for an organization that already exists, it is necessary to discover its technological components. Then the collected data should be treated and stored in the CMDB chosen by the organization. Thus, the main goal is to develop a method for automatic creation of a CMDB, using network analysis tools, machine audits, and system inventory.

Taking into account the technology products that implement CMDB, it is necessary to adapt the data to the structure of this database to be used by the organization.

## Folder Structure

Structured in several modules:

* models: contains the models definitions
    * Attribute
    * ConfigurationItem
* password_vault
* normalization
* reconciliation
* basic_discovery
* execution_queue
* discovery_mechanisms
* db_population
* cmdb_processor
* db_processor
* similarity
* semantic_matching
* syntatic_matching
* model_mapper
* cmdb_population
