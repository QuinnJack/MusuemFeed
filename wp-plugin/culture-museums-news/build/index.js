( function ( wp ) {
const { registerBlockType } = wp.blocks;
const { __ } = wp.i18n;
const { InspectorControls } = wp.blockEditor || wp.editor;
const { PanelBody, TextControl, SelectControl } = wp.components;

registerBlockType( 'cmn/news-grid', {
title: __( 'Museum News Grid', 'cmn' ),
icon: 'grid-view',
category: 'widgets',
attributes: {
region: { type: 'string', default: 'canada' },
layout: { type: 'string', default: 'grid' },
count: { type: 'number', default: 6 },
},
edit: ( props ) => {
const { attributes, setAttributes } = props;

return (
<div className="cmn-news-grid-placeholder">
<InspectorControls>
<PanelBody title={ __( 'Feed settings', 'cmn' ) }>
<TextControl
label={ __( 'Region', 'cmn' ) }
value={ attributes.region }
onChange={ ( value ) => setAttributes( { region: value } ) }
/>
<SelectControl
label={ __( 'Layout', 'cmn' ) }
value={ attributes.layout }
options={ [
{ label: __( 'Grid', 'cmn' ), value: 'grid' },
{ label: __( 'Big main + 2 small', 'cmn' ), value: 'big-main-2-small' },
{ label: __( 'Photo only', 'cmn' ), value: 'photo-only' },
] }
onChange={ ( value ) => setAttributes( { layout: value } ) }
/>
<TextControl
type="number"
label={ __( 'Count', 'cmn' ) }
value={ attributes.count }
onChange={ ( value ) => setAttributes( { count: parseInt( value, 10 ) || 0 } ) }
/>
</PanelBody>
</InspectorControls>
<p>{ __( 'Museum news will render on the front-end based on the ingestion service.', 'cmn' ) }</p>
</div>
);
},
save: () => null,
} );
} )( window.wp );
