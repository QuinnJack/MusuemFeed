<?php
/**
 * Plugin Name: Culture Museums News Hub
 * Description: Custom post type, REST endpoints, and Gutenberg blocks for museum news aggregation.
 * Version: 0.1.0
 * Author: Culture Museums
 */

defined('ABSPATH') || exit;

define('CMN_PLUGIN_PATH', plugin_dir_path(__FILE__));

define('CMN_PLUGIN_URL', plugin_dir_url(__FILE__));

require_once CMN_PLUGIN_PATH . 'includes/class-cmn-post-type.php';
require_once CMN_PLUGIN_PATH . 'includes/class-cmn-rest-controller.php';
require_once CMN_PLUGIN_PATH . 'includes/class-cmn-settings.php';
require_once CMN_PLUGIN_PATH . 'includes/class-cmn-blocks.php';

function cmn_bootstrap(): void {
    \CMN\Post_Type::init();
    \CMN\REST_Controller::init();
    \CMN\Settings::init();
    \CMN\Blocks::init();
}
add_action('plugins_loaded', 'cmn_bootstrap');
