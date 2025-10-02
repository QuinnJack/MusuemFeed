<?php
namespace CMN;
defined('ABSPATH') || exit;

/**
 * Proxy REST controller for exposing curated news in WordPress.
 */
class REST_Controller {
    private const NAMESPACE = 'cm/v1';

    public static function init(): void {
        add_action('rest_api_init', [self::class, 'register_routes']);
    }

    public static function register_routes(): void {
        register_rest_route(self::NAMESPACE, '/news', [
            'methods' => 'GET',
            'callback' => [self::class, 'get_news'],
            'permission_callback' => '__return_true',
            'args' => [
                'region' => ['type' => 'string', 'required' => false],
                'topics' => ['type' => 'array', 'items' => ['type' => 'string']],
                'count' => ['type' => 'integer', 'default' => 6],
                'language' => ['type' => 'string'],
                'min_score' => ['type' => 'number'],
                'layout' => ['type' => 'string'],
            ],
        ]);
    }

    public static function get_news(\WP_REST_Request $request): \WP_REST_Response {
        $query_args = [
            'post_type' => 'cm_news_item',
            'posts_per_page' => $request['count'] ?? 6,
            'post_status' => 'publish',
            'meta_query' => [],
        ];

        if ($request['region']) {
            $query_args['meta_query'][] = [
                'key' => 'region',
                'value' => sanitize_text_field($request['region']),
            ];
        }

        if ($request['language']) {
            $query_args['meta_query'][] = [
                'key' => 'language',
                'value' => sanitize_text_field($request['language']),
            ];
        }

        $query = new \WP_Query($query_args);
        $items = [];

        foreach ($query->posts as $post) {
            $items[] = [
                'id' => $post->ID,
                'title' => get_the_title($post),
                'summary' => get_the_excerpt($post),
                'source' => get_post_meta($post->ID, 'source', true),
                'published_at' => get_post_meta($post->ID, 'published_at', true),
                'image_url' => get_the_post_thumbnail_url($post, 'full'),
                'region' => get_post_meta($post->ID, 'region', true),
                'topics' => (array) get_post_meta($post->ID, 'topics', true),
                'score' => (float) get_post_meta($post->ID, 'score', true),
                'language' => get_post_meta($post->ID, 'language', true),
                'canonical_url' => get_post_meta($post->ID, 'canonical_url', true),
                'ai_generated_image' => (bool) get_post_meta($post->ID, 'ai_generated_image', true),
            ];
        }

        return new \WP_REST_Response([
            'items' => $items,
            'meta' => [
                'count' => count($items),
                'layout' => $request['layout'] ?? 'grid',
            ],
        ]);
    }
}
