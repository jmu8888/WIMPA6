<?php
/**
 * WIMPA 6 theme setup.
 */

define( 'WIMPA6_VERSION', '1.0.0' );
// Default location of the winners gallery images (the GitHub Pages copy of the site).
define( 'WIMPA6_IMG_DEFAULT', 'https://jmu8888.github.io/WIMPA6/images/' );

add_action( 'after_setup_theme', function () {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
	register_nav_menus( array(
		'primary'    => 'Main menu (English)',
		'primary_zh' => 'Main menu (Chinese)',
	) );
} );

/** Is the current page part of the Chinese site (the "zh" page or one of its children)? */
function wimpa6_is_zh() {
	if ( ! is_page() ) {
		return false;
	}
	$post = get_queried_object();
	if ( 'zh' === $post->post_name ) {
		return true;
	}
	foreach ( get_post_ancestors( $post ) as $id ) {
		if ( 'zh' === get_post_field( 'post_name', $id ) ) {
			return true;
		}
	}
	return false;
}

/** Which part of the site this is, used by site.js (home, winners, archive, enter, jury, about, legacy). */
function wimpa6_page_kind() {
	if ( is_front_page() ) {
		return 'home';
	}
	if ( is_page() ) {
		$kind = get_post_meta( get_queried_object_id(), 'wimpa_page', true );
		if ( $kind ) {
			return $kind;
		}
	}
	return 'legacy';
}

/** URL of a page by its path, e.g. "rules" or "zh/rules". */
function wimpa6_url( $path ) {
	$page = get_page_by_path( $path );
	return $page ? get_permalink( $page ) : home_url( '/?pagename=' . $path );
}

/** The same page in the other language, or that language's home page. */
function wimpa6_other_lang_url() {
	if ( is_page() ) {
		$pair = get_post_meta( get_queried_object_id(), 'wimpa_pair', true );
		if ( $pair ) {
			return 'home' === $pair ? home_url( '/' ) : wimpa6_url( $pair );
		}
	}
	return wimpa6_is_zh() ? home_url( '/' ) : wimpa6_url( 'zh' );
}

add_action( 'wp_enqueue_scripts', function () {
	$uri = get_template_directory_uri();
	wp_enqueue_style( 'wimpa6-fonts', 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@500;600&display=swap', array(), null );
	wp_enqueue_style( 'wimpa6-site', $uri . '/assets/site.css', array(), WIMPA6_VERSION );
	wp_enqueue_style( 'wimpa6-wp', $uri . '/assets/wp.css', array( 'wimpa6-site' ), WIMPA6_VERSION );

	$zh  = wimpa6_is_zh();
	$pre = $zh ? 'zh/' : '';
	wp_enqueue_script( 'wimpa6-data', $uri . '/assets/data.js', array(), WIMPA6_VERSION, true );
	wp_enqueue_script( 'wimpa6-site', $uri . '/assets/site.js', array( 'wimpa6-data' ), WIMPA6_VERSION, true );
	wp_localize_script( 'wimpa6-data', 'WIMPA_CONF', array(
		'img'   => trailingslashit( get_theme_mod( 'wimpa6_img_base', WIMPA6_IMG_DEFAULT ) ),
		'lang'  => $zh ? 'zh' : 'en',
		'links' => array(
			'winners' => wimpa6_url( $pre . 'winners' ),
			'archive' => wimpa6_url( $pre . 'past-winners' ),
			'enter'   => wimpa6_url( $pre . 'rules' ),
		),
	) );
} );

/** Customizer: where the winners gallery images are served from. */
add_action( 'customize_register', function ( $wp_customize ) {
	$wp_customize->add_section( 'wimpa6', array( 'title' => 'WIMPA gallery images', 'priority' => 160 ) );
	$wp_customize->add_setting( 'wimpa6_img_base', array( 'default' => WIMPA6_IMG_DEFAULT, 'sanitize_callback' => 'esc_url_raw' ) );
	$wp_customize->add_control( 'wimpa6_img_base', array(
		'section'     => 'wimpa6',
		'label'       => 'Images folder URL',
		'description' => 'Folder that contains the w/ and t/ image folders. Default: the GitHub Pages copy. If you upload the images folder to this server, enter its URL here.',
		'type'        => 'url',
	) );
} );

/** Show the menu for a language; falls back to the menu named "WIMPA Main" / "WIMPA 中文" when no location is set. */
function wimpa6_menu( $zh ) {
	$location = $zh ? 'primary_zh' : 'primary';
	$args     = array( 'container' => false, 'menu_class' => 'menu', 'depth' => 3, 'fallback_cb' => false, 'echo' => false );
	if ( has_nav_menu( $location ) ) {
		return wp_nav_menu( $args + array( 'theme_location' => $location ) );
	}
	$menu = wp_get_nav_menu_object( $zh ? 'WIMPA 中文' : 'WIMPA Main' );
	return $menu ? wp_nav_menu( $args + array( 'menu' => $menu->term_id ) ) : '';
}

// New WIMPA pages carry their own layout; keep WordPress from adding <p> tags inside it.
add_filter( 'the_content', function ( $content ) {
	if ( is_page() && get_post_meta( get_the_ID(), 'wimpa_page', true ) ) {
		remove_filter( 'the_content', 'wpautop' );
	}
	return $content;
}, 0 );
