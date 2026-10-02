<?php
$wimpa_zh = wimpa6_is_zh();
$p        = $wimpa_zh ? 'zh/' : '';
$explore  = $wimpa_zh
	? array( 'winners' => '第五届获奖作品', 'past-winners' => '往届获奖作品', 'rules' => '参赛类别与规则', 'jury' => '评委', 'about' => '关于大赛' )
	: array( 'winners' => '5th Winners', 'past-winners' => 'Past Winners', 'rules' => 'Categories & Rules', 'jury' => 'Jury', 'about' => 'About' );
$more     = $wimpa_zh
	? array( 'previous-awards' => '往届大赛（2021–2025）', 'sponsors' => '赞助商', 'co-organizer-list' => '协办单位', 'donation' => '捐款支持' )
	: array( 'previous-awards' => 'Previous Awards (2021–2025)', 'sponsors' => 'Sponsors', 'co-organizer-list' => 'Co-Organizers', 'donation' => 'Donation' );
?>
<footer class="ftr">
	<div class="wrap">
		<div class="cols">
			<div>
				<a class="logo" href="<?php echo esc_url( $wimpa_zh ? wimpa6_url( 'zh' ) : home_url( '/' ) ); ?>"><b><?php echo $wimpa_zh ? '第六届 WIMPA' : '6th WIMPA'; ?></b></a>
				<p style="margin-top:14px;max-width:340px"><?php echo $wimpa_zh ? '华盛顿国际手机摄影大赛：为世界各地的手机摄影爱好者搭建平台，用一帧帧影像讲述身边的故事。' : 'The Washington International Mobile Photography Awards: a platform for mobile photographers everywhere to tell the stories around them, one frame at a time.'; ?></p>
			</div>
			<div><h4><?php echo $wimpa_zh ? '浏览' : 'Explore'; ?></h4>
				<?php foreach ( $explore as $slug => $label ) : ?><a href="<?php echo esc_url( wimpa6_url( $p . $slug ) ); ?>"><?php echo esc_html( $label ); ?></a><?php endforeach; ?>
			</div>
			<div><h4><?php echo $wimpa_zh ? '更多' : 'More'; ?></h4>
				<?php foreach ( $more as $slug => $label ) : ?><a href="<?php echo esc_url( wimpa6_url( $slug ) ); ?>"><?php echo esc_html( $label ); ?></a><?php endforeach; ?>
			</div>
			<div><h4><?php echo $wimpa_zh ? '联系我们' : 'Contact'; ?></h4>
				<a href="mailto:info.wcaf@gmail.com">info.wcaf@gmail.com</a>
				<a href="https://www.gwmpa.org/login"><?php echo $wimpa_zh ? '投稿系统' : 'Submission system'; ?></a>
				<a href="<?php echo esc_url( wimpa6_other_lang_url() ); ?>"><?php echo $wimpa_zh ? 'English' : '中文'; ?></a>
				<p style="margin-top:12px"><?php echo $wimpa_zh ? '主办单位：华盛顿文化艺术基金会（WCAF）' : 'Organized by the Washington Cultural Arts Foundation (WCAF)'; ?></p>
			</div>
		</div>
		<div class="legal"><span>&copy; 2021&ndash;<?php echo esc_html( gmdate( 'Y' ) ); ?> <?php echo $wimpa_zh ? '华盛顿国际手机摄影大赛 版权所有。' : 'Washington International Mobile Photography Awards. All rights reserved.'; ?></span><span><?php echo $wimpa_zh ? '所有摄影作品版权归原作者所有，未经许可不得使用。' : 'All photographs are copyright of their respective photographers and may not be used without permission.'; ?></span></div>
	</div>
</footer>
<?php wp_footer(); ?>
</body>
</html>
