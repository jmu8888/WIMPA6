<?php
$wimpa_zh = wimpa6_is_zh();
$wimpa_home = $wimpa_zh ? wimpa6_url( 'zh' ) : home_url( '/' );
?><!doctype html>
<html lang="<?php echo $wimpa_zh ? 'zh-CN' : 'en'; ?>">
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?> data-page="<?php echo esc_attr( wimpa6_page_kind() ); ?>">
<?php wp_body_open(); ?>
<header class="hdr">
	<div class="wrap">
		<a class="logo" href="<?php echo esc_url( $wimpa_home ); ?>"><b><?php echo $wimpa_zh ? '第六届 WIMPA' : '6th WIMPA'; ?></b><span><?php echo $wimpa_zh ? '华盛顿国际手机摄影大赛' : 'Washington International Mobile Photography Awards'; ?></span></a>
		<div class="hright">
			<a class="lang" href="<?php echo esc_url( wimpa6_other_lang_url() ); ?>" lang="<?php echo $wimpa_zh ? 'en' : 'zh-CN'; ?>"><?php echo $wimpa_zh ? 'English' : '中文'; ?></a>
			<button class="burger" aria-label="Menu" onclick="this.closest('.wrap').querySelector('.nav').classList.toggle('open')">&#9776;</button>
		</div>
		<nav class="nav">
			<?php echo wimpa6_menu( $wimpa_zh ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			<a class="btn" href="<?php echo esc_url( wimpa6_url( ( $wimpa_zh ? 'zh/' : '' ) . 'rules' ) . '#submit' ); ?>"><?php echo $wimpa_zh ? '立即参赛' : 'Enter Now'; ?></a>
		</nav>
	</div>
</header>
