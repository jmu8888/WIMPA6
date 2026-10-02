<?php
/**
 * Front page: shows the English home page (the page with slug "wimpa-home"),
 * whatever Settings > Reading says.
 */
get_header();
$home = get_page_by_path( 'wimpa-home' );
if ( $home ) {
	echo apply_filters( 'the_content', $home->post_content ); // phpcs:ignore WordPress.Security.EscapeOutput
} elseif ( have_posts() ) {
	while ( have_posts() ) {
		the_post();
		the_content();
	}
}
get_footer();
