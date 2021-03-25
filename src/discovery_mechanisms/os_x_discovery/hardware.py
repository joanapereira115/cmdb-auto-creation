# -*- coding: utf-8 -*-

import regex
import json
from colored import fg, attr

from models import ConfigurationItem, ConfigurationItemType, Relationship, RelationshipType, methods

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')


def hw_discovery(client, ci):
    """
    Gathers information about the hardware (physical ports, energy, displays, ...) of the OS X machine.

    Parameters
    ----------
    client: SSHClient
        The SSH client that permits the comunication with the machine that is being explored.

    ci: ConfigurationItem
        The configuration item that represents the OS X machine that is going to be explored.
    """
    _, stdout, stderr = client.exec_command(
        "networksetup -listallhardwareports")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset +
              "Error while collecting information about ports: " + str(error) + "\n")
    else:
        hw_ports = stdout.readlines()
        hw_ports_info = "".join(hw_ports).split("\n")
        for line in hw_ports_info:
            line = line.strip("\n")
            if regex.search(r'Hardware Port', line, regex.IGNORECASE) != None:
                hw_port_type = methods.add_ci_type(
                    ConfigurationItemType.ConfigurationItemType("Hardware Port"))
                obj = ConfigurationItem.ConfigurationItem()
                obj.set_type(hw_port_type.get_id())
                name = line[len("Hardware Port:"):].strip(" ")
                obj.set_title(name)

            elif regex.search(r'Device', line, regex.IGNORECASE) != None:
                ifc = line[len("Device:"):].strip(" ")
                methods.define_attribute("interface", ifc, obj)

            elif regex.search(r'Ethernet Address', line, regex.IGNORECASE) != None:
                address = line[len("Ethernet Address:"):].strip(" ")
                ipv6 = regex.search(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))', address)
                ipv4 = regex.search(
                    r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])', address)
                mac = regex.search(
                    r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', address)
                if ipv6 != None:
                    obj.add_ipv6_address(address)
                elif ipv4 != None:
                    obj.add_ipv4_address(address)
                elif mac != None:
                    obj.set_mac_address(address)

                rel_type_ci_obj = methods.add_rel_type(
                    RelationshipType.RelationshipType("has hardware port"))
                rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
                rel_ci_obj.title = str(ci.get_title()) + \
                    " has hardware port " + str(obj.get_title())

                rel_type_obj_ci = methods.add_rel_type(
                    RelationshipType.RelationshipType("port on device"))
                rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
                rel_obj_ci.title = str(obj.get_title()) + \
                    " port on device " + str(ci.get_title())

                methods.add_ci(obj)
                methods.add_rel(rel_ci_obj)
                methods.add_rel(rel_obj_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPPowerDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset +
              "Error while collecting information about power: " + str(error) + "\n")
    else:
        power = stdout.readlines()
        power_info = json.loads("".join(power)).get('SPPowerDataType')
        for pinfo in power_info:
            if pinfo.get("_name") == "spbattery_information":
                battery_type = methods.add_ci_type(
                    ConfigurationItemType.ConfigurationItemType("Battery"))
                bat_obj = ConfigurationItem.ConfigurationItem()
                bat_obj.set_type(battery_type.get_id())

                methods.define_attribute("current capacity", pinfo.get(
                    "sppower_battery_charge_info").get("sppower_battery_current_capacity"), bat_obj)
                methods.define_attribute("fully charged", pinfo.get(
                    "sppower_battery_charge_info").get("sppower_battery_fully_charged"), bat_obj)
                methods.define_attribute("is charging", pinfo.get(
                    "sppower_battery_charge_info").get("sppower_battery_is_charging"), bat_obj)
                methods.define_attribute("max capacity", pinfo.get(
                    "sppower_battery_charge_info").get("sppower_battery_max_capacity"), bat_obj)
                methods.define_attribute("cycle count", pinfo.get(
                    "sppower_battery_health_info").get("sppower_battery_cycle_count"), bat_obj)
                methods.define_attribute("status", pinfo.get(
                    "sppower_battery_health_info").get("sppower_battery_health"), bat_obj)
                methods.define_attribute("installed", pinfo.get(
                    "sppower_battery_installed"), bat_obj)
                methods.define_attribute("Pack Lot Code", pinfo.get(
                    "sppower_battery_model_info").get("Pack Lot Code"), bat_obj)
                methods.define_attribute("PCB Lot Code", pinfo.get(
                    "sppower_battery_model_info").get("PCB Lot Code"), bat_obj)
                methods.define_attribute("cell revision", pinfo.get(
                    "sppower_battery_model_info").get("sppower_battery_cell_revision"), bat_obj)
                methods.define_attribute("firmware version", pinfo.get(
                    "sppower_battery_model_info").get("sppower_battery_firmware_version"), bat_obj)
                methods.define_attribute("hardware revision", pinfo.get(
                    "sppower_battery_model_info").get("sppower_battery_hardware_revision"), bat_obj)
                methods.define_attribute("serial number", pinfo.get(
                    "sppower_battery_model_info").get("sppower_battery_serial_number"), bat_obj)

                name = pinfo.get("sppower_battery_model_info").get(
                    "sppower_battery_device_name")
                methods.define_attribute("battery", name, ci)
                bat_obj.set_title(name)
                manufacturer = pinfo.get("sppower_battery_model_info").get(
                    "sppower_battery_manufacturer")
                methods.define_attribute("manufacturer", manufacturer, bat_obj)

                manufacturer_type = methods.add_ci_type(
                    ConfigurationItemType.ConfigurationItemType("Manufacturer"))
                man_obj = ConfigurationItem.ConfigurationItem()
                man_obj.set_title(manufacturer)
                man_obj.set_type(manufacturer_type.get_id())

                rel_type_bat_man = methods.add_rel_type(
                    RelationshipType.RelationshipType("has manufacturer"))
                rel_bat_man = methods.create_relation(
                    bat_obj, man_obj, rel_type_bat_man)
                rel_bat_man.title = str(bat_obj.get_title()) + \
                    " has manufacturer " + str(man_obj.get_title())

                rel_type_man_bat = methods.add_rel_type(
                    RelationshipType.RelationshipType("manufacturer of"))
                rel_man_bat = methods.create_relation(
                    man_obj, bat_obj, rel_type_man_bat)
                rel_man_bat.title = str(man_obj.get_title()) + \
                    " manufacturer of " + str(bat_obj.get_title())

                methods.add_ci(bat_obj)
                methods.add_ci(man_obj)
                methods.add_rel(rel_bat_man)
                methods.add_rel(rel_man_bat)

                methods.define_attribute("current amperage", pinfo.get(
                    "sppower_current_amperage"), bat_obj)
                methods.define_attribute("current voltage", pinfo.get(
                    "sppower_current_voltage"), bat_obj)

                rel_type_ci_bat = methods.add_rel_type(
                    RelationshipType.RelationshipType("has battery"))
                rel_ci_bat = methods.create_relation(
                    ci, bat_obj, rel_type_ci_bat)
                rel_ci_bat.title = str(ci.get_title()) + \
                    " has battery " + str(bat_obj.get_title())

                rel_type_bat_ci = methods.add_rel_type(
                    RelationshipType.RelationshipType("battery of"))
                rel_bat_ci = methods.create_relation(
                    bat_obj, ci, rel_type_bat_ci)
                rel_bat_ci.title = str(bat_obj.get_title()) + \
                    " battery of " + str(ci.get_title())

                methods.add_rel(rel_ci_bat)
                methods.add_rel(rel_bat_ci)

            if pinfo.get("_name") == "sppower_information":
                ac_type = methods.add_ci_type(
                    ConfigurationItemType.ConfigurationItemType("Charger"))
                ac_obj = ConfigurationItem.ConfigurationItem()
                ac_obj.set_type(ac_type.get_id())

                ac_info = pinfo.get("AC Power")
                methods.define_attribute(
                    "Auto Power Off Delay", ac_info.get("AutoPowerOff Delay"), ac_obj)
                methods.define_attribute(
                    "Auto Power Off Enabled", ac_info.get("AutoPowerOff Enabled"), ac_obj)
                methods.define_attribute(
                    "Current Power Source", ac_info.get("Current Power Source"), ac_obj)
                methods.define_attribute(
                    "Dark Wake Background Tasks", ac_info.get("DarkWakeBackgroundTasks"), ac_obj)
                methods.define_attribute(
                    "Disk Sleep Timer", ac_info.get("Disk Sleep Timer"), ac_obj)
                methods.define_attribute(
                    "Display Sleep Timer", ac_info.get("Display Sleep Timer"), ac_obj)
                methods.define_attribute(
                    "Display Sleep Uses Dim", ac_info.get("Display Sleep Uses Dim"), ac_obj)
                methods.define_attribute(
                    "GPU Switch", ac_info.get("GPUSwitch"), ac_obj)
                methods.define_attribute(
                    "Hibernate Mode", ac_info.get("Hibernate Mode"), ac_obj)
                methods.define_attribute(
                    "High Standby Delay", ac_info.get("High Standby Delay"), ac_obj)
                methods.define_attribute(
                    "Prioritize Network Reachability Over Sleep", ac_info.get("PrioritizeNetworkReachabilityOverSleep"), ac_obj)
                methods.define_attribute(
                    "Proximity Dark Wake", ac_info.get("ProximityDarkWake"), ac_obj)
                methods.define_attribute(
                    "Reduce Brightness", ac_info.get("ReduceBrightness"), ac_obj)
                methods.define_attribute(
                    "Standby Battery Threshold", ac_info.get("Standby Battery Threshold"), ac_obj)
                methods.define_attribute(
                    "Standby Delay", ac_info.get("Standby Delay"), ac_obj)
                methods.define_attribute(
                    "Standby Enabled", ac_info.get("Standby Enabled"), ac_obj)
                methods.define_attribute(
                    "System Sleep Timer", ac_info.get("System Sleep Timer"), ac_obj)
                methods.define_attribute(
                    "TCP Keep Alive Pref", ac_info.get("TCPKeepAlivePref"), ac_obj)
                methods.define_attribute(
                    "Wake On AC Change", ac_info.get("Wake On AC Change"), ac_obj)
                methods.define_attribute(
                    "Wake On Clamshell Open", ac_info.get("Wake On Clamshell Open"), ac_obj)
                methods.define_attribute(
                    "Wake On LAN", ac_info.get("Wake On LAN"), ac_obj)

                bat_info = pinfo.get("Battery Power")
                methods.define_attribute(
                    "Auto Power Off Delay", bat_info.get("AutoPowerOff Delay"), bat_obj)
                methods.define_attribute(
                    "Auto Power Off Enabled", bat_info.get("AutoPowerOff Enabled"), bat_obj)
                methods.define_attribute(
                    "Dark Wake Background Tasks", bat_info.get("DarkWakeBackgroundTasks"), bat_obj)
                methods.define_attribute(
                    "Disk Sleep Timer", bat_info.get("Disk Sleep Timer"), bat_obj)
                methods.define_attribute(
                    "Display Sleep Timer", bat_info.get("Display Sleep Timer"), bat_obj)
                methods.define_attribute(
                    "Display Sleep Uses Dim", bat_info.get("Display Sleep Uses Dim"), bat_obj)
                methods.define_attribute(
                    "GPU Switch", bat_info.get("GPUSwitch"), bat_obj)
                methods.define_attribute(
                    "Hibernate Mode", bat_info.get("Hibernate Mode"), bat_obj)
                methods.define_attribute(
                    "High Standby Delay", bat_info.get("High Standby Delay"), bat_obj)
                methods.define_attribute(
                    "Proximity Dark Wake", bat_info.get("ProximityDarkWake"), bat_obj)
                methods.define_attribute(
                    "Reduce Brightness", bat_info.get("ReduceBrightness"), bat_obj)
                methods.define_attribute(
                    "Standby Battery Threshold", bat_info.get("Standby Battery Threshold"), bat_obj)
                methods.define_attribute(
                    "Standby Delay", bat_info.get("Standby Delay"), bat_obj)
                methods.define_attribute(
                    "Standby Enabled", bat_info.get("Standby Enabled"), bat_obj)
                methods.define_attribute(
                    "System Sleep Timer", bat_info.get("System Sleep Timer"), bat_obj)
                methods.define_attribute(
                    "TCP Keep Alive Pref", bat_info.get("TCPKeepAlivePref"), bat_obj)
                methods.define_attribute(
                    "Wake On AC Change", bat_info.get("Wake On AC Change"), bat_obj)
                methods.define_attribute(
                    "Wake On Clamshell Open", bat_info.get("Wake On Clamshell Open"), bat_obj)

                methods.add_ci(ac_obj)
                methods.add_ci(bat_obj)

            if pinfo.get("_name") == "sppower_ac_charger_information":
                methods.define_attribute(
                    "family", pinfo.get("sppower_ac_charger_family"), ac_obj)
                ac_obj.set_title(pinfo.get("sppower_ac_charger_ID"))
                methods.define_attribute(
                    "charger", pinfo.get("sppower_ac_charger_ID"), ci)
                methods.define_attribute(
                    "serial number", pinfo.get("sppower_ac_charger_serial_number"), ac_obj)
                methods.define_attribute(
                    "watts", pinfo.get("sppower_ac_charger_watts"), ac_obj)
                methods.define_attribute(
                    "connected", pinfo.get("sppower_battery_charger_connected"), ac_obj)
                methods.define_attribute(
                    "charging", pinfo.get("sppower_battery_is_charging"), ac_obj)

                rel_type_ci_ac = methods.add_rel_type(
                    RelationshipType.RelationshipType("has charger"))
                rel_ci_ac = methods.create_relation(
                    ci, ac_obj, rel_type_ci_ac)
                rel_ci_ac.title = str(ci.get_title()) + \
                    " has charger " + str(ac_obj.get_title())

                rel_type_ac_ci = methods.add_rel_type(
                    RelationshipType.RelationshipType("charger of"))
                rel_ac_ci = methods.create_relation(
                    ac_obj, ci, rel_type_ac_ci)
                rel_ac_ci.title = str(ac_obj.get_title()) + \
                    " charger of " + str(ci.get_title())

                methods.add_ci(ac_obj)
                methods.add_rel(rel_ci_ac)
                methods.add_rel(rel_ac_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPAudioDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset +
              "Error while collecting information about audio: " + str(error) + "\n")
    else:
        audio = stdout.readlines()
        audio_info = json.loads("".join(audio)).get('SPAudioDataType')[0]
        for aud in audio_info.get("_items"):
            audio_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType(aud.get("_name")))
            obj = ConfigurationItem.ConfigurationItem()
            obj.set_type(audio_type.get_id())
            obj.set_title(aud.get("_name"))

            methods.define_attribute("default audio input device", aud.get(
                "coreaudio_default_audio_input_device"), obj)
            methods.define_attribute(
                "device input", aud.get("coreaudio_device_input"), obj)
            methods.define_attribute(
                "srate", aud.get("coreaudio_device_srate"), obj)
            methods.define_attribute(
                "transport", aud.get("coreaudio_device_transport"), obj)
            methods.define_attribute(
                "input source", aud.get("coreaudio_input_source"), obj)
            methods.define_attribute(
                "properties", aud.get("_properties"), obj)
            methods.define_attribute("default audio output_device", aud.get(
                "coreaudio_default_audio_output_device"), obj)
            methods.define_attribute("default audio system device", aud.get(
                "coreaudio_default_audio_system_device"), obj)
            methods.define_attribute("device output", aud.get(
                "coreaudio_device_output"), obj)
            methods.define_attribute("output source", aud.get(
                "coreaudio_output_source"), obj)

            manufacturer = aud.get("coreaudio_device_manufacturer")
            methods.define_attribute("manufacturer", manufacturer, obj)
            manufacturer_type = methods.add_ci_type(
                ConfigurationItemType.ConfigurationItemType("Manufacturer"))
            man_obj = ConfigurationItem.ConfigurationItem()
            man_obj.set_title(manufacturer)
            man_obj.set_type(manufacturer_type.get_id())

            rel_type_obj_man = methods.add_rel_type(
                RelationshipType.RelationshipType("has manufacturer"))
            rel_obj_man = methods.create_relation(
                obj, man_obj, rel_type_obj_man)
            rel_obj_man.title = str(obj.get_title()) + \
                " has manufacturer " + str(man_obj.get_title())

            rel_type_man_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("manufacturer of"))
            rel_man_obj = methods.create_relation(
                man_obj, obj, rel_type_man_obj)
            rel_man_obj.title = str(man_obj.get_title()) + \
                " manufacturer of " + str(obj.get_title())

            methods.add_ci(obj)
            methods.add_ci(man_obj)
            methods.add_rel(rel_obj_man)
            methods.add_rel(rel_man_obj)

            rel_type_ci_obj = methods.add_rel_type(
                RelationshipType.RelationshipType("has " + str(aud.get("_name"))))
            rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
            rel_ci_obj.title = str(ci.get_title()) + \
                " associated " + str(aud.get("_name")) + \
                " " + str(obj.get_title())

            rel_type_obj_ci = methods.add_rel_type(
                RelationshipType.RelationshipType(str(aud.get("_name") + " of")))
            rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
            rel_obj_ci.title = str(
                obj.get_title()) + " " + str(aud.get("_name")) + " of " + str(ci.get_title())

            methods.add_rel(rel_ci_obj)
            methods.add_rel(rel_obj_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPCameraDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset +
              "Error while collecting information about cameras: " + str(error) + "\n")
    else:
        cam = stdout.readlines()
        cam_info = json.loads("".join(cam)).get('SPCameraDataType')[0]

        cam_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("Camera"))
        obj = ConfigurationItem.ConfigurationItem()
        obj.set_type(cam_type.get_id())
        obj.set_title(cam_info.get("_name"))
        methods.define_attribute("camera", cam_info.get("_name"), ci)

        methods.define_attribute("model", cam_info.get(
            "spcamera_model-id"), obj)
        methods.define_attribute("uuid", cam_info.get(
            "spcamera_unique-id"), obj)

        rel_type_ci_obj = methods.add_rel_type(
            RelationshipType.RelationshipType("associated camera"))
        rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
        rel_ci_obj.title = str(ci.get_title()) + \
            " associated camera " + str(obj.get_title())

        rel_type_obj_ci = methods.add_rel_type(
            RelationshipType.RelationshipType("camera of"))
        rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
        rel_obj_ci.title = str(obj.get_title()) + \
            " camera of " + str(ci.get_title())

        methods.add_ci(obj)
        methods.add_rel(rel_ci_obj)
        methods.add_rel(rel_obj_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPCardReaderDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        card = stdout.readlines()
        card_info = json.loads("".join(card)).get('SPCardReaderDataType')[0]

        card_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType(card_info.get("_name")))
        obj = ConfigurationItem.ConfigurationItem()
        obj.set_type(card_type.get_id())
        obj.set_title(card_info.get("_name"))

        methods.define_attribute("product id", card_info.get(
            "spcardreader_product-id"), obj)
        methods.define_attribute("revision id", card_info.get(
            "spcardreader_revision-id"), obj)
        methods.define_attribute("serial number", card_info.get(
            "spcardreader_serialnumber"), obj)
        methods.define_attribute("vendor id", card_info.get(
            "spcardreader_vendor-id"), obj)

        if len(card_info.get("_items")) > 0:
            if len(card_info.get("_items")[0].get("volumes")) > 0:
                volumes = card_info.get("_items")[0].get("volumes")
                for vol in volumes:
                    card_type = methods.add_ci_type(
                        ConfigurationItemType.ConfigurationItemType(vol.get("_name")))
                    card = ConfigurationItem.ConfigurationItem()
                    for at in vol:
                        if at == "_name":
                            card.set_title(vol.get(at))
                        else:
                            methods.define_attribute(at, vol.get(at), card)

                    rel_type_obj_card = methods.add_rel_type(
                        RelationshipType.RelationshipType("reading card"))
                    rel_obj_card = methods.create_relation(
                        obj, card, rel_type_obj_card)
                    rel_obj_card.title = str(obj.get_title()) + \
                        " reading card " + str(card.get_title())

                    rel_type_card_obj = methods.add_rel_type(
                        RelationshipType.RelationshipType("card reading by"))
                    rel_card_obj = methods.create_relation(
                        card, obj, rel_type_card_obj)
                    rel_card_obj.title = str(card.get_title()) + \
                        " card reading by " + str(obj.get_title())

                    methods.add_ci(card)
                    methods.add_rel(rel_obj_card)
                    methods.add_rel(rel_card_obj)

        rel_type_ci_obj = methods.add_rel_type(
            RelationshipType.RelationshipType("associated card reader"))
        rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
        rel_ci_obj.title = str(ci.get_title()) + \
            " associated card reader " + str(obj.get_title())

        rel_type_obj_ci = methods.add_rel_type(
            RelationshipType.RelationshipType("card reader of"))
        rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
        rel_obj_ci.title = str(obj.get_title()) + \
            " card reader of " + str(ci.get_title())

        methods.add_ci(obj)
        methods.add_rel(rel_ci_obj)
        methods.add_rel(rel_obj_ci)
###########################################
    _, stdout, stderr = client.exec_command(
        "system_profiler SPDisplaysDataType -json")
    error = stderr.read().decode('utf-8')
    if error != "":
        print(red + ">>> " + reset + str(error) + "\n")
    else:
        display = stdout.readlines()
        display_info = json.loads("".join(display)).get(
            'SPDisplaysDataType')[0].get("spdisplays_ndrvs")[0]

        display_type = methods.add_ci_type(
            ConfigurationItemType.ConfigurationItemType("Display"))
        obj = ConfigurationItem.ConfigurationItem()
        obj.set_type(display_type.get_id())

        obj.set_title(display_info.get("_name"))
        methods.define_attribute("display", display_info.get("_name"), ci)

        methods.define_attribute("pixels", display_info.get(
            "_spdisplays_pixels"), obj)
        methods.define_attribute("year", display_info.get(
            "_spdisplays_display-year"), obj)
        methods.define_attribute("resolution", display_info.get(
            "_spdisplays_resolution"), obj)
        methods.define_attribute("pixel resolution", display_info.get(
            "spdisplays_pixelresolution"), obj)
        methods.define_attribute("connection type", display_info.get(
            "spdisplays_connection_type"), obj)
        methods.define_attribute("depth", display_info.get(
            "spdisplays_depth"), obj)
        methods.define_attribute("display type", display_info.get(
            "spdisplays_display_type"), obj)

        rel_type_ci_obj = methods.add_rel_type(
            RelationshipType.RelationshipType("associated display"))
        rel_ci_obj = methods.create_relation(ci, obj, rel_type_ci_obj)
        rel_ci_obj.title = str(ci.get_title()) + \
            " associated display " + str(obj.get_title())

        rel_type_obj_ci = methods.add_rel_type(
            RelationshipType.RelationshipType("display of"))
        rel_obj_ci = methods.create_relation(obj, ci, rel_type_obj_ci)
        rel_obj_ci.title = str(obj.get_title()) + \
            " display of " + str(ci.get_title())

        methods.add_ci(obj)
        methods.add_rel(rel_ci_obj)
        methods.add_rel(rel_obj_ci)
