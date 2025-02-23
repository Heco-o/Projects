#include <dpp/dpp.h>
#include <fstream>
#include <nlohmann/json.hpp>

nlohmann::json T;
nlohmann::json data;
std::ifstream file("/data/data/com.termux/files/home/TOKEN.json");
std::ifstream file2("data.json");

void saveData() {
	std::ofstream file("data.json");
	file << std::setw(4) << data;
	file.close();
}

std::vector<std::string> board = { "_", "_", "_", "_", "_", "_", "_", "_", "_" };
std::string current_player = "X"; // Track the current player (X or O)

void update_board(dpp::cluster& bot, const dpp::button_click_t& event) {
	
}

int main() {
	if (!file.is_open() || !file2.is_open()) {
		std::cerr << "Failed to open file!\n" + std::to_string(file.is_open()) + "\n" + std::to_string(file2.is_open());
		return 1;
	} 

	try {
		file >> T;
		file2 >> data;
		file.close();
		file2.close();
	} catch (const std::exception& e) {
		std::cerr << "Failed to parse JSON.\n" << e.what();
		return 1;
	}
	
	dpp::cluster bot(T["B"], dpp::i_default_intents);
	
	bot.on_log(dpp::utility::cout_logger());
	
	bot.on_slashcommand([&bot](const dpp::slashcommand_t& event) {
		if (event.command.usr.id == "870748995872518155") {
			const dpp::snowflake guildID = event.command.guild_id;
			const std::string sGuildID = std::to_string(guildID);
			if (event.command.get_command_name() == "ping") {
				event.reply("Pong!");
			} else if (event.command.get_command_name() == "test") {
				bot.channel_get(event.command.channel_id, [event](const dpp::confirmation_callback_t& callback) {
					std::string roles;
					const auto perms = callback.get<dpp::channel>().permission_overwrites;
					if (perms.size() > 0) {
						for (const auto& perm : perms) {
							if (perm.type == dpp::ot_role) {
								roles += "<@&" + std::to_string(perm.id) + ">\n";
							} else {
								roles += "<@" + std::to_string(perm.id) + ">\n";
							}
							roles += "allowed: `" + std::to_string(perm.allow) + "`\n";
							roles += "denied: `" + std::to_string(perm.deny) + "`\n";
						}
						roles.erase(roles.size() - 1);
						event.reply(roles);
					} else {
						event.reply("No permission overwrite was found.");
					}
				});
			} else if (event.command.get_command_name() == "test1") {
				bot.channel_get(event.command.channel_id, [&bot, event](const dpp::confirmation_callback_t& callback) {
					const dpp::snowflake categoryID = callback.get<dpp::channel>().parent_id;
					bot.channels_get(event.command.guild_id, [event, categoryID](const dpp::confirmation_callback_t& callback) {
						std::string names;
						const dpp::channel_map channels = callback.get<dpp::channel_map>();
						for (const auto& pair : channels) {
							if (pair.second.parent_id == categoryID) {
								names += "name: `" + pair.second.name + "`, id: `" + std::to_string(pair.first) + "`\n";
							}
						}
						names.erase(names.size() - 1);
						event.reply(names);
					});
				});
			} else if (event.command.get_command_name() == "serverlock") {
				if (data[sGuildID] == nullptr) {
					bot.channels_get(guildID, [&bot, event, guildID, sGuildID](const dpp::confirmation_callback_t& callback) {
						const dpp::channel_map mChannels = callback.get<dpp::channel_map>();
						for (const auto pair : mChannels) {
							const std::string sChannelID = std::to_string(pair.first);
							const dpp::channel channel = pair.second;
							dpp::permission allow;
							dpp::permission deny;
							
							if (channel.permission_overwrites.size() > 0) {
								bool check = false;
								for (const dpp::permission_overwrite overPerm : channel.permission_overwrites) {
									if (overPerm.id == guildID) {
										allow = overPerm.allow;
										deny = overPerm.deny;
										if (allow.can(dpp::p_send_messages)) {
											data[sGuildID][sChannelID]["sendMsg"] = true;
											allow.remove(dpp::p_send_messages);
											deny.add(dpp::p_send_messages);
										} else if (deny.can(dpp::p_send_messages)) {
											data[sGuildID][sChannelID]["sendMsg"] = false;
										} else {
											data[sGuildID][sChannelID]["sendMsg"] = nullptr;
											deny.add(dpp::p_send_messages);
										}
										check = true;
										break;
									}
								} if (!check) {
									data[sGuildID][sChannelID] = nullptr;
									deny.add(dpp::p_send_messages);
								}
							} else {
								data[sGuildID][sChannelID] = nullptr;
								deny.add(dpp::p_send_messages);
							}
							bot.channel_edit_permissions(channel, guildID, allow, deny, false, [channel](const dpp::confirmation_callback_t& callback) {
								if (callback.is_error()) {
									std::cerr << "Lock: " << callback.get_error().message << std::endl;
								} else {
									std::cout << "Lock -> " << channel.name << ": success!" << std::endl;
								}
							});
						}
						dpp::message m;
						m.guild_id = guildID;
						m.channel_id = event.command.channel_id;
						m.content = "Server has been locked.";
						bot.message_create(m);
						saveData();
					});
				} else {
					event.reply("Server is already locked.");
				}
				std::cout << "ServerLock: success!" << std::endl;
				event.reply("Server is being locked...");
			} else if (event.command.get_command_name() == "serverunlock") {
				if (data[sGuildID] != nullptr) {
					bot.channels_get(guildID, [&bot, event, guildID, sGuildID](const dpp::confirmation_callback_t& callback) {
						const dpp::channel_map mChannels = callback.get<dpp::channel_map>();
						for (const auto pair : mChannels) {
							const std::string sChannelID = std::to_string(pair.first);
							if (data[sGuildID].find(sChannelID) == data[sGuildID].end()) {
								continue;
							}
							const dpp::channel channel = pair.second;
							dpp::permission allow;
							dpp::permission deny;
							
							if (data[sGuildID][sChannelID] != nullptr) {
								for (const auto overPerm : channel.permission_overwrites) {
									if (overPerm.id == guildID) {
										allow = overPerm.allow;
										deny = overPerm.deny;
									}
								}
								if (data[sGuildID][sChannelID]["sendMsg"] == true) {
									allow.add(dpp::p_send_messages);
									deny.remove(dpp::p_send_messages);
								} else if (data[sGuildID][sChannelID]["sendMsg"] == nullptr) {
									deny.remove(dpp::p_send_messages);
								} if (data[sGuildID][sChannelID]["sendMsg"] != false) {
									bot.channel_edit_permissions(channel, guildID, allow, deny, false, [channel](const dpp::confirmation_callback_t& callback) {
										if (callback.is_error()) {
											std::cerr << "UnLock: " << callback.get_error().message << std::endl;
										} else {
											std::cout << "UnLock -> " << channel.name << ": success!" << std::endl;
										}
									});
								}
							} else {
								bot.channel_delete_permission(channel, guildID, [channel](const dpp::confirmation_callback_t& callback) {
									if (callback.is_error()) {
										std::cerr << "Remove: " << callback.get_error().message << std::endl;
									} else {
										std::cout << "Remove -> " << channel.name << ": success!" << std::endl;
									}
								});
							}
						}
						dpp::message m;
						m.guild_id = guildID;
						m.channel_id = event.command.channel_id;
						m.content = "Server has been unlocked.";
						bot.message_create(m);
						data[sGuildID] = nullptr;
						saveData();
					});
					std::cout << "ServerUnLock: success!" << std::endl;
					event.reply("Server is being unlocked...");
				} else {
					event.reply("You didn't lock the server.");
				}
			}
		}
	});
	
	bot.on_ready([&bot](const dpp::ready_t& event) {
		if (dpp::run_once<struct register_bot_commands>()) {
			//bot.global_bulk_command_delete();
			bot.global_command_create(dpp::slashcommand("ping", "Ping pong!", bot.me.id));
			bot.global_command_create(dpp::slashcommand("test", "test", bot.me.id));
			bot.global_command_create(dpp::slashcommand("test1", "test1", bot.me.id));
			bot.global_command_create(dpp::slashcommand("serverlock", "locks the server", bot.me.id));
			bot.global_command_create(dpp::slashcommand("serverunlock", "unlocks the server", bot.me.id));
			bot.global_command_create(dpp::slashcommand("tic-tac-toe", "Play a tic-tac-toe game witht the perfect bot.", bot.me.id));
		}
	});
	
	bot.start(dpp::st_wait);
}