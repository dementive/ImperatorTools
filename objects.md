# Imperator Game Objects

# TODO - add scripted_lists and treasure game objects

### area

scope - area:

area_list = ["area", "is_in_area", "owns_or_subject_owns_area", "owns_area"]

### region

scope - region:

region_list = ["region", "owns_or_subject_owns_region", "owns_region", "is_in_region"]

### ambitions
a_list = ["set_ambition","has_ambition"]

### buildings

# TODO - custom parsing that finds the province rank in the allow and puts it in the completion details

b_list = ["can_build_building","has_building", "add_building_level"]

### cultures

# TODO - add a culture group attribute to cultures so they can show it in completion details

scope - culture:

c_list = ["set_culture","set_pop_culture","set_primary_culture", "culture"]

### Culture Group

scope - culture_group:

### deathreasons

death_list = ["death_reason"]

### deities

# TODO - Custom parsing for deities that finds the religion of the deity and puts it in autocomplete details

scopes - deity:

### diplomatic_stances

diplo_list = ["diplomatic_stance"]

### economic_policies

econ_list = ["has_low_economic_policy", "has_mid_economic_policy", "has_high_economic_policy"]

### event_pictures

event_pic_list = ["picture"]

### event_themes

event_theme_list = ["theme"]

### governments

gov_list = ["government", "change_government"]

### governor_policies

gov_policy_list = ["governor_policy", "can_change_governor_policy"]

### heritage

heritage_list = ["heritage", "set_country_heritage"]

### ideas

idea_list = ["can_change_idea", "idea"]

### inventions

invention_list = ["invention"]

requires_or = { commerce_inv_5 }
requires = { commerce_inv_5 }

### laws

law_list = ["has_law","change_law"]

### legion_distinctions

distinction_list = ["has_distinction"]

### levy_templates

levy_list = ["levy_template"]

### loyalty

loyalty_list["can_add_entire_loyalty_bonus","has_loyalty","remove_loyalty","add_loyalty"]

### military_traditions

tradition_list = ["has_military_bonus"]

### missions

has_completed_mission

### mission tasks

has_completed_mission_task

### modifiers
modifiers_list = [
	"has_unit_modifier","has_country_modifier","has_province_modifier","has_character_modifier",
	"has_triggered_character_modifier","has_state_modifier","has_country_culture_modifier",
	"remove_triggered_character_modifier","remove_country_modifier","remove_province_modifier",
	"add_country_modifier", "remove_unit_modifier","remove_character_modifier","add_unit_modifier",
	"add_permanent_province_modifier","add_province_modifier","remove_state_modifier",
	"add_character_modifier","add_state_modifier","add_triggered_character_modifier",
]

### opinions

opinion_list = ["has_opinion"]
remove_opinion = {
    modifier = <opinion>
}
reverse_add_opinion = {
    modifier = <opinion>
}
add_opinion = {
    modifier = <opinion>
}

### offices

office_list = ["give_office","remove_office","can_hold_office","office_is_empty","has_office"]

### party_types

scope - party:

party_list = ["remove_party_leadership","party","is_leader_of_party","is_leader_of_party_type","party_type","has_party_type","is_party_type"]

add_party_support = {
    party = <party_type>
}
add_party_conviction = {
    party = <party_type>
}

### pop_types

pop_list = ["create_pop","set_pop_type","create_state_pop","pop_type","has_pop_type_right","is_pop_type_right"]

define_pop = {
    type = <pop_type>
}

### prices

price_list = ["subject_pays","pay_price","refund_price","can_pay_price"]

### province_ranks

prov_rank_list = ["set_city_status", "has_province_rank"]

### religions

scope - religion:

religion_list = [
	"set_character_religion","set_pop_religion","set_country_religion",
	"has_religion","pop_religion","religion","dominant_province_religion",
	"deity_religion","religion",
]

### script_values

### scripted_effects

### scripted_modifiers

### scripted_triggers

### subject_types

subjects_list = ["is_subject_type"]

make_subject = {
    type = <subject_type>
}

### technology_tables

tech_table_list = ["has_tech_office_of"]
add_research = {
    technology = <technology_table>
}

### terrain_types
terrain_list = ["terrain"]

### trade_goods


goods_list = ["set_trade_goods","can_import_trade_good","trade_goods","is_importing_trade_good"]
trade_good_surplus = {
    target = <trade_goods>
}


### traits

traits_list = ["force_add_trait","add_trait","remove_trait","has_trait"]

opposites = {
	good_natured
}

### treasures

# TODO - make game objects and find a way to parse these.

treasure_list = [
	"destroy_treasure","transfer_treasure_to_character",
	"transfer_treasure_to_country","transfer_treasure_to_province","create_country_treasure"
]


### units

unit_list = ["add_loyal_subunit","add_subunit","is_dominant_unit","sub_unit_type"]

num_of_unit_type = {
    type = <unit_type>
}

### wargoals

declare_war_with_wargoal = {
    war_goal = <war_goal>
}