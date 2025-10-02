<?php
namespace CMN;
defined('ABSPATH') || exit;

/**
 * Register the custom post type used to store curated news items.
 */
class Post_Type {
    public static function init(): void {
        add_action('init', [self::class, 'register']);
    }

    public static function register(): void {
        register_post_type('cm_news_item', [
            'labels' => [
                'name' => __('Museum News', 'cmn'),
                'singular_name' => __('Museum News Item', 'cmn'),
            ],
            'public' => false,
            'show_ui' => true,
            'supports' => ['title', 'editor', 'excerpt', 'thumbnail', 'custom-fields'],
            'show_in_rest' => true,
            'menu_icon' => 'dashicons-admin-site',
        ]);
    }
}
