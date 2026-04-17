import xml.etree.ElementTree as ET
from datetime import datetime

def merge_gpx_two_pointers(from_path, to_path, output_path, params_to_merge, creator=None):
    # Standard namespaces
    ns = {
        'default': 'http://www.topografix.com/GPX/1/1',
        'gpxtpx': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'
    }
    
    for prefix, uri in ns.items():
        ET.register_namespace(prefix if prefix != 'default' else '', uri)

    tree_to = ET.parse(to_path)
    tree_from = ET.parse(from_path)

    if creator is not None:
        root = tree_to.getroot()
        root.set('creator', creator)
    
    # Get all track points from both files
    points_to = tree_to.findall('.//default:trkpt', ns)
    points_from = tree_from.findall('.//default:trkpt', ns)

    idx1 = 0
    idx2 = 0

    while idx1 < len(points_to) and idx2 < len(points_from):
        # Extract times
        time_str1 = points_to[idx1].find('default:time', ns).text
        time_str2 = points_from[idx2].find('default:time', ns).text
        
        # Convert to datetime for safe comparison
        t1 = datetime.fromisoformat(time_str1.replace('Z', '+00:00'))
        t2 = datetime.fromisoformat(time_str2.replace('Z', '+00:00'))

        if t1 == t2:
            # Sync: Copy extensions from FROM to TO
            sync_extensions(points_to[idx1], points_from[idx2], params_to_merge, ns)
            idx1 += 1
            idx2 += 1
        elif t1 < t2:
            # TO is behind, move TO pointer forward
            idx1 += 1
        else:
            # FROM is behind, move FROM pointer forward
            idx2 += 1

    # Save results
    tree_to.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Merge complete. Saved to {output_path}")

def sync_extensions(target_pt, source_pt, params, ns):
    """Injects specific parameters from source_pt to target_pt."""
    
    # Ensure <extensions> and <gpxtpx:TrackPointExtension> exist in target
    ext_node = target_pt.find('default:extensions', ns)
    if ext_node is None:
        ext_node = ET.SubElement(target_pt, f'{{{ns["default"]}}}extensions')

    tpx_target = ext_node.find('gpxtpx:TrackPointExtension', ns)
    if tpx_target is None:
        tpx_target = ET.SubElement(ext_node, f'{{{ns["gpxtpx"]}}}TrackPointExtension')

    # Look for the source TrackPointExtension
    tpx_source = source_pt.find('.//gpxtpx:TrackPointExtension', ns)
    if tpx_source is None:
        return

    for param in params:
        source_param_node = tpx_source.find(f'gpxtpx:{param}', ns)
        if source_param_node is not None:
            # Check if it already exists in target, if so update, otherwise create
            target_param_node = tpx_target.find(f'gpxtpx:{param}', ns)
            if target_param_node is None:
                target_param_node = ET.SubElement(tpx_target, f'{{{ns["gpxtpx"]}}}{param}')
            target_param_node.text = source_param_node.text

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge GPX extension parameters from FROM into TO, synchronized by time.")
    parser.add_argument("from_file", help="FROM GPX file (source of extension parameters)")
    parser.add_argument("to", help="TO GPX file (base geometry/track kept)")
    parser.add_argument("output", help="Output GPX file name")
    parser.add_argument("params", nargs='+', help="List of parameter names to merge (e.g. hr cad)")
    parser.add_argument("--creator", default=None, help="Value for the GPX creator attribute (optional)")
    args = parser.parse_args()

    merge_gpx_two_pointers(args.from_file, args.to, args.output, args.params, creator=args.creator)