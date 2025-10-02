<?php
namespace CMN;
defined('ABSPATH') || exit;

/**
 * Admin settings page for mapping feeds and thresholds.
 */
class Settings {
    public const OPTION = 'cmn_settings';

    public static function init(): void {
        add_action('admin_menu', [self::class, 'register_menu']);
        add_action('admin_init', [self::class, 'register_settings']);
    }

    public static function register_menu(): void {
        add_options_page(
            __('Culture Museums News', 'cmn'),
            __('Culture Museums News', 'cmn'),
            'manage_options',
            'cmn-settings',
            [self::class, 'render_page']
        );
    }

    public static function register_settings(): void {
        register_setting(self::OPTION, self::OPTION, [self::class, 'sanitize']);

        add_settings_section('cmn_main', __('Feed configuration', 'cmn'), function (): void {
            echo '<p>' . esc_html__('Configure ingestion service endpoints and thresholds.', 'cmn') . '</p>';
        }, 'cmn-settings');

        add_settings_field('ingestion_url', __('Ingestion API URL', 'cmn'), function () {
            $options = get_option(self::OPTION);
            $value = $options['ingestion_url'] ?? '';
            printf('<input type="url" name="%s[ingestion_url]" value="%s" class="regular-text" />', esc_attr(self::OPTION), esc_url($value));
        }, 'cmn-settings', 'cmn_main');

        add_settings_field('regions', __('Region presets', 'cmn'), function () {
            $options = get_option(self::OPTION);
            $value = $options['regions'] ?? '';
            printf('<textarea name="%s[regions]" rows="5" class="large-text code">%s</textarea>', esc_attr(self::OPTION), esc_textarea($value));
            echo '<p class="description">' . esc_html__('Provide JSON mapping of regions to feed sources.', 'cmn') . '</p>';
        }, 'cmn-settings', 'cmn_main');
    }

    public static function sanitize(array $input): array {
        $output = [];
        $output['ingestion_url'] = esc_url_raw($input['ingestion_url'] ?? '');
        $output['regions'] = wp_kses_post($input['regions'] ?? '');
        return $output;
    }

    public static function render_page(): void {
        ?>
        <div class="wrap">
            <h1><?php echo esc_html__('Culture Museums News Settings', 'cmn'); ?></h1>
            <form action="options.php" method="post">
                <?php
                settings_fields(self::OPTION);
                do_settings_sections('cmn-settings');
                submit_button();
                ?>
            </form>
        </div>
        <?php
    }
}
