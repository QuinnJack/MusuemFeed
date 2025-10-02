<?php
namespace CMN;
defined('ABSPATH') || exit;

/**
 * Gutenberg block registration hooks.
 */
class Blocks {
    public static function init(): void {
        add_action('init', [self::class, 'register_assets']);
        add_action('enqueue_block_editor_assets', [self::class, 'enqueue_editor_assets']);
    }

    public static function register_assets(): void {
        wp_register_script(
            'cmn-blocks-editor',
            CMN_PLUGIN_URL . 'build/index.js',
            ['wp-blocks', 'wp-element', 'wp-components', 'wp-data', 'wp-editor'],
            '0.1.0',
            true
        );

        register_block_type('cmn/news-grid', [
            'editor_script' => 'cmn-blocks-editor',
            'render_callback' => [self::class, 'render_news_grid'],
            'attributes' => [
                'region' => ['type' => 'string', 'default' => 'canada'],
                'layout' => ['type' => 'string', 'default' => 'grid'],
                'count' => ['type' => 'number', 'default' => 6],
            ],
        ]);
    }

    public static function enqueue_editor_assets(): void {
        wp_enqueue_script('cmn-blocks-editor');
    }

    public static function render_news_grid(array $attributes, string $content): string {
        $api_url = get_option(Settings::OPTION)['ingestion_url'] ?? '';
        $region = sanitize_text_field($attributes['region'] ?? 'canada');
        $count = absint($attributes['count'] ?? 6);
        $layout = sanitize_text_field($attributes['layout'] ?? 'grid');

        $cache_key = sprintf('cmn_block_%s_%s_%d', $region, $layout, $count);
        $cached = get_transient($cache_key);
        if ($cached) {
            return $cached;
        }

        $items = self::fetch_items($api_url, [
            'region' => $region,
            'count' => $count,
            'layout' => $layout,
        ]);

        ob_start();
        ?>
        <div class="cmn-news-grid layout-<?php echo esc_attr($layout); ?>">
            <?php foreach ($items as $item) : ?>
                <article class="cmn-news-item">
                    <?php if (!empty($item['image_url'])) : ?>
                        <figure class="cmn-news-item__image">
                            <img src="<?php echo esc_url($item['image_url']); ?>" alt="<?php echo esc_attr($item['title']); ?>">
                        </figure>
                    <?php endif; ?>
                    <header>
                        <h3><?php echo esc_html($item['title']); ?></h3>
                        <p class="cmn-news-item__meta">
                            <?php echo esc_html($item['source']); ?> · <?php echo esc_html(gmdate('Y-m-d', strtotime($item['published_at']))); ?>
                        </p>
                    </header>
                    <p class="cmn-news-item__summary"><?php echo esc_html($item['summary']); ?></p>
                    <?php if (!empty($item['canonical_url'])) : ?>
                        <p><a href="<?php echo esc_url($item['canonical_url']); ?>" class="cmn-news-item__link" target="_blank" rel="noopener">Read more</a></p>
                    <?php endif; ?>
                </article>
            <?php endforeach; ?>
        </div>
        <?php
        $markup = ob_get_clean();
        set_transient($cache_key, $markup, HOUR_IN_SECONDS);
        return $markup;
    }

    private static function fetch_items(string $api_url, array $params): array {
        if (empty($api_url)) {
            return [];
        }

        $response = wp_remote_get(add_query_arg($params, trailingslashit($api_url) . 'articles'));
        if (is_wp_error($response)) {
            return [];
        }

        $body = json_decode(wp_remote_retrieve_body($response), true);
        return $body['items'] ?? [];
    }
}
