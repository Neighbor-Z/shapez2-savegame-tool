import os
import uuid
import json
import zipfile
from io import BytesIO
from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__)
UPLOAD_FOLDER = 'sessions'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

TARGET_FILES = ['savegame.json', 'local-player.json', 'research.json']

MILESTONE_MAPPING = {
    "RNInitial": "Milestone_Initial",
    # "RNStackerLayer2": "Milestone_SpaceFloor3",
    "RNBlueprints": "CBSandbox",
    "RNRotatorCCW": "CBRotating_ReverseRotator",
    "RNHalvesSwapper": "CBCutting_Swapper",
    "RNFullCutter": "CBCutting_FullCutter",
    "RNTrash": "CBBelts_Trash",
    "RNIslandBuilding": "Milestone_Initial",
    "RNRotatorHalf": "CBRotating_Rotator180",
    "RNBentStacker": "CBStacking_BentStacker",
    "RNWireBasics": "CBWires_Core",
    "RNWireLogicGates": "CBWires_LogicGates",
    "RNFluids": "Milestone_FluidPainting",
    "RNWireVirtualProcessing": "CBWires_VirtualProcessing",
    "RNFluidTank": "CBFluids_Storage",
    # "RNIslandLayouts1": "CBPlatformPack_Linear",
    "RNTrains": "Milestone_ShapeTrains",
    # "RNLayer3": "Milestone_SpaceFloor3",
    "RNPinPusher": "Milestone_PinPusher",
    "RNColorMixing": "Milestone_ColorMixing",
    "RNWireTransmission": "CBWires_UniversalTransmission",
    "RNLabel": "CBDecorations_Labels",
    "RNCrystals": "Milestone_Crystals",
    "RNTrainsFluidWagons": "CBTrains_FluidTransport",
    "RNTrainHubDelivery": "Milestone_VortexDelivery",
    "RNEndOfGame": "Milestone_FinalConverters",
    # "RNIslandLayouts2": "CBPlatformPack_Irregular",
    # "RNIslandLayouts3": "CBPlatformPack_Blocky",
    # "RNIslandLayouts4": "CBPlatformPack_Large",
    "RNRailRollerCoasterDLCContent": "DLCBTrains_RailRollerCoaster",
    "RNTrainsFillerWagon": "CBTrains_EmptyTransport",
    "RNOverflowSplitter": "CBBelts_OverflowSplitter",
    "RNTrainsWaitStop": "CBTrains_TrainStopHalting",
    "RNWireOperatorReceiver": "CBWires_GoalReceiver",
    # "RNIslandLayer3": "SG_IslandLayer3_1_1",
    "RNTrainsPrimaryColors": "CBTrains_LinePackPrimary",
    "RNTrainsSecondaryColors": "CBTrains_LinePackSecondary",
    "RNTrainsTertiaryColors": "CBTrains_LineWhite",
    "RNTrainsTransferStation": "CBTrains_TransferStations",
}

VALID_NEW_MILESTONES = {
    'Milestone_Initial', 
    'Milestone_FluidPainting', 
    'Milestone_ShapeTrains', 
    'Milestone_PinPusher', 
    'Milestone_ColorMixing', 
    'Milestone_SpaceFloor3', 
    'Milestone_Crystals', 
    'Milestone_VortexDelivery', 
    'Milestone_FinalConverters', 
    'Milestone_PostFinal_Tier0', 
    'Milestone_PostFinal_Tier1', 
    'Milestone_PostFinal_Tier2', 
    'Milestone_PostFinal_Tier3', 
    'CBSandbox', 
    'CBCutting_FullCutter', 
    'CBCutting_Swapper', 
    'CBBelts_Trash', 
    'CBRotating_ReverseRotator', 
    'CBRotating_Rotator180', 
    'CBStacking_BentStacker', 
    'CBBelts_OverflowSplitter', 
    'CBSpecial_FactoryFloor3', 
    'CBFluids_Storage', 
    'CBDecorations_Labels', 
    'CBWires_Core', 
    'CBWires_LogicGates', 
    'CBWires_VirtualProcessing', 
    'CBWires_UniversalTransmission', 
    'CBWires_GoalReceiver', 
    'CBPlatformPack_Linear', 
    'CBPlatformPack_Irregular', 
    'CBPlatformPack_Blocky', 
    'CBPlatformPack_Large', 
    'CBTrains_FluidTransport', 
    'CBTrains_EmptyTransport', 
    'CBTrains_TrainStopHalting', 
    'CBTrains_TransferStations', 
    'CBTrains_StationSpacer', 
    'CBTrains_LinePackPrimary', 
    'CBTrains_LinePackSecondary', 
    'CBTrains_LineWhite', 
    'DLCBTrains_RailRollerCoaster', 
    'SG_Islands_1_1', 'SG_Islands_1_2', 'SG_Islands_1_3', 'SG_Islands_1_4', 
    'SG_Islands_2_1', 'SG_Islands_2_2', 'SG_Islands_2_3', 'SG_Islands_2_4', 'SG_Islands_2_5', 
    'SG_Islands_3_1', 'SG_Islands_3_2', 'SG_Islands_3_3', 'SG_Islands_3_4', 
    'SG_Islands_4_1', 'SG_Islands_4_2', 'SG_Islands_4_3', 'SG_Islands_4_4', 'SG_Islands_4_5', 
    'SG_Fluids_1_1', 'SG_Fluids_1_2', 'SG_Fluids_1_3', 'SG_Fluids_1_4', 'SG_Fluids_1_5', 
    'SG_Fluids_2_1', 'SG_Fluids_2_2', 'SG_Fluids_2_3', 'SG_Fluids_2_4', 'SG_Fluids_2_5', 
    'SG_Fluids_3_1', 'SG_Fluids_3_2', 'SG_Fluids_3_3', 'SG_Fluids_3_4', 'SG_Fluids_3_5', 
    'SG_Fluids_4_1', 'SG_Fluids_4_2', 'SG_Fluids_4_3', 'SG_Fluids_4_4', 'SG_Fluids_4_5', 
    'SG_Trains_1_1', 'SG_Trains_1_2', 'SG_Trains_1_3', 'SG_Trains_1_4', 'SG_Trains_1_5', 
    'SG_Trains_2_1', 'SG_Trains_2_2', 'SG_Trains_2_3', 'SG_Trains_2_4', 'SG_Trains_2_5', 
    'SG_Trains_3_1', 'SG_Trains_3_2', 'SG_Trains_3_3', 'SG_Trains_3_4', 
    'SG_Trains_4_1', 'SG_Trains_4_2', 'SG_Trains_4_3', 'SG_Trains_4_4', 'SG_Trains_4_5', 
    'SG_Trains_6_1', 'SG_Trains_6_2', 'SG_Trains_6_3', 'SG_Trains_6_4', 'SG_Trains_6_5', 
    'SG_PinPusher_2_1', 'SG_PinPusher_2_2', 'SG_PinPusher_2_3', 'SG_PinPusher_2_4', 
    'SG_PinPusher_3_1', 'SG_PinPusher_3_2', 'SG_PinPusher_3_3', 'SG_PinPusher_3_4', 'SG_PinPusher_3_5', 
    'SG_PinPusher_4_1', 'SG_PinPusher_4_2', 'SG_PinPusher_4_3', 'SG_PinPusher_4_4', 
    'SG_PinPusher_5_1', 'SG_PinPusher_5_2', 'SG_PinPusher_5_3', 'SG_PinPusher_5_4', 'SG_PinPusher_5_5', 
    'SG_Mixing_1_1', 'SG_Mixing_1_2', 'SG_Mixing_1_3', 'SG_Mixing_1_4', 'SG_Mixing_1_5', 
    'SG_Mixing_2_1', 'SG_Mixing_2_2', 'SG_Mixing_2_3', 'SG_Mixing_2_4', 
    'SG_Mixing_3_1', 'SG_Mixing_3_2', 'SG_Mixing_3_3', 
    'SG_Mixing_4_1', 'SG_Mixing_4_2', 'SG_Mixing_4_3', 'SG_Mixing_4_4', 
    'SG_Mixing_5_1', 'SG_Mixing_5_2', 'SG_Mixing_5_3', 'SG_Mixing_5_4', 'SG_Mixing_5_5', 
    'SG_Mixing_6_1', 'SG_Mixing_6_2', 'SG_Mixing_6_3', 'SG_Mixing_6_4', 'SG_Mixing_6_5', 
    'SG_Mixing_7_1', 'SG_Mixing_7_2', 'SG_Mixing_7_3', 'SG_Mixing_7_4', 'SG_Mixing_7_5', 
    'SG_IslandLayer3_1_1', 'SG_IslandLayer3_1_2', 'SG_IslandLayer3_1_3', 'SG_IslandLayer3_1_4', 'SG_IslandLayer3_1_5', 
    'SG_IslandLayer3_2_1', 'SG_IslandLayer3_2_2', 'SG_IslandLayer3_2_3', 'SG_IslandLayer3_2_4', 'SG_IslandLayer3_2_5', 
    'SG_Crystals_1_1', 'SG_Crystals_1_2', 'SG_Crystals_1_3', 'SG_Crystals_1_4', 'SG_Crystals_1_5', 
    'SG_Crystals_2_1', 'SG_Crystals_2_2', 'SG_Crystals_2_3', 'SG_Crystals_2_4', 'SG_Crystals_2_5', 
    'SG_Crystals_3_1', 'SG_Crystals_3_2', 'SG_Crystals_3_3', 'SG_Crystals_3_4', 'SG_Crystals_3_5', 
    'SG_TrainHubDelivery_1_1', 'SG_TrainHubDelivery_1_2', 'SG_TrainHubDelivery_1_3', 'SG_TrainHubDelivery_1_4', 'SG_TrainHubDelivery_1_5', 
    'SG_TrainHubDelivery_2_1', 'SG_TrainHubDelivery_2_2', 'SG_TrainHubDelivery_2_3', 'SG_TrainHubDelivery_2_4', 'SG_TrainHubDelivery_2_5', 
    'SG_PostFinalT0_1_1', 'SG_PostFinalT0_1_2', 'SG_PostFinalT0_1_3', 'SG_PostFinalT0_1_4', 
    'SG_PostFinalT0_2_1', 'SG_PostFinalT0_2_2', 'SG_PostFinalT0_2_3', 'SG_PostFinalT0_2_4', 'SG_PostFinalT0_2_5', 
    'SG_PostFinalT1_1_1', 'SG_PostFinalT1_1_2', 'SG_PostFinalT1_1_3', 'SG_PostFinalT1_1_4', 'SG_PostFinalT1_1_5', 
    'SG_PostFinalT1_2_1', 'SG_PostFinalT1_2_2', 'SG_PostFinalT1_2_3', 'SG_PostFinalT1_2_4', 
    'SG_PostFinalT2_1_1', 'SG_PostFinalT2_1_2', 'SG_PostFinalT2_1_3', 'SG_PostFinalT2_1_4', 
    'SG_PostFinalT2_2_1', 'SG_PostFinalT2_2_2', 'SG_PostFinalT2_2_3', 'SG_PostFinalT2_2_4', 
    'SG_PostFinalT3_1_1', 'SG_PostFinalT3_1_2', 'SG_PostFinalT3_1_3', 'SG_PostFinalT3_1_4'
}

def migrate_milestones(old_nodes):
    new_nodes = set()
    for node in old_nodes:
        # Use mapping if exists, otherwise keep original node if it's still valid
        mapped_node = MILESTONE_MAPPING.get(node, node)
        if mapped_node in VALID_NEW_MILESTONES:
            new_nodes.add(mapped_node)
    return sorted(list(new_nodes))

@app.route('/')
def index():
    return render_template('index_flask.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    session_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_FOLDER, f"{session_id}.spz2")
    file.save(save_path)
    
    jsons = {}
    try:
        with zipfile.ZipFile(save_path, 'r') as zf:
            for target in TARGET_FILES:
                if target in zf.namelist():
                    data = zf.read(target).decode('utf-8')
                    jsons[target] = json.loads(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    return jsonify({
        'session_id': session_id,
        'files': jsons
    })

@app.route('/api/upgrade_ng_plus', methods=['POST'])
def upgrade_save_ng_plus():
    data = request.json
    session_id = data.get('session_id')
    force = data.get('force', False)

    if not session_id:
        return jsonify({'error': 'Missing session_id'}), 400
        
    original_path = os.path.join(UPLOAD_FOLDER, f"{session_id}.spz2")
    if not os.path.exists(original_path):
        return jsonify({'error': 'Session expired or not found'}), 404

    template_path = "template-v1.spz2"
    
    if not os.path.exists(template_path):
        return jsonify({'error': 'Template file missing from server!'}), 500
        
    memory_file = BytesIO()
    try:
        with zipfile.ZipFile(original_path, 'r') as zin_old:
            with zipfile.ZipFile(template_path, 'r') as zin_template:
                with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zout:
                    
                    # 1. READ OLD DATA
                    try:
                        old_research = json.loads(zin_old.read("research.json").decode('utf-8'))
                    except:
                        old_research = {}
                        
                    try:
                        old_savegame = json.loads(zin_old.read("savegame.json").decode('utf-8'))
                    except:
                        old_savegame = {}
                        
                    try:
                        old_player = json.loads(zin_old.read("local-player.json").decode('utf-8'))
                    except:
                        old_player = {}

                    # 2. READ TEMPLATE DATA
                    template_savegame = json.loads(zin_template.read("savegame.json").decode('utf-8'))
                    template_research = json.loads(zin_template.read("research.json").decode('utf-8'))
                    template_player = json.loads(zin_template.read("local-player.json").decode('utf-8'))

                    # --- Check for parameter mismatches ---
                    old_params = old_savegame.get("Parameters", {})
                    temp_params = template_savegame.get("Parameters", {})
                    
                    diff = {}
                    for key in ["GameModeId", "Seed"]:
                        old_val = old_params.get(key)
                        temp_val = temp_params.get(key)
                        if old_val != temp_val:
                            diff[key] = {"old": old_val, "template": temp_val}
                    
                    if diff and not force:
                        return jsonify({
                            "needs_confirmation": True,
                            "diff": diff
                        })

                    # 3. GRAFT NEW GAME+ DATA into template structure

                    # --- savegame.json ---
                    # We KEEP the seed and parameters from the template to ensure the newly generated map is valid.
                    # We bring over the progress flags.
                    template_savegame["InternalUuid"] = old_savegame.get("InternalUuid", template_savegame.get("InternalUuid"))
                    template_savegame["LastSaved"] = old_savegame.get("LastSaved", template_savegame.get("LastSaved"))
                    template_savegame["SavegameName"] = old_savegame.get("SavegameName", "NG_Plus_Save") + "_NG+"
                    template_savegame["TotalPlaytime"] = old_savegame.get("TotalPlaytime", 0)
                    template_savegame["ResearchProgress"] = old_savegame.get("ResearchProgress", 0)
                    template_savegame["StructureCount"] = 0 # It's a blank NG+ map!
                    
                    # --- local-player.json ---
                    # HUD Data removal fix (deprecated Wiki)
                    if "HUDData" in old_player and "Wiki" in old_player["HUDData"]:
                        del old_player["HUDData"]["Wiki"]
                    if "HUDData" in old_player and "TutorialState" not in old_player["HUDData"]:
                        old_player["HUDData"]["TutorialState"] = {"CompletedTutorials": []}
                    template_player = old_player # Keep entire player UI layout config otherwise

                    # --- research.json ---
                    # Heuristic Unlock injection
                    player_level = old_research.get("PlayerLevel", {}).get("Level", 0)
                    # Merge currencies and levels into template
                    template_research["PlayerLevel"] = old_research.get("PlayerLevel", template_research.get("PlayerLevel", {}))
                    template_research["PointCurrency"] = old_research.get("PointCurrency", template_research.get("PointCurrency", {}))
                    if "TotalSpent" not in template_research["PointCurrency"]:
                        template_research["PointCurrency"]["TotalSpent"] = 0

                    if "ResearchProgress" in old_research and "UnlockedUpgradeIds" in old_research["ResearchProgress"]:
                        # Prepare mapped milestones
                        old_nodes = old_research["ResearchProgress"]["UnlockedUpgradeIds"]
                        template_research.setdefault("ResearchProgress", {})["UnlockedUpgradeIds"] = migrate_milestones(old_nodes)
                    else:
                        template_research.setdefault("ResearchProgress", {})["UnlockedUpgradeIds"] = ["Milestone_Initial"]

                    # if 'LinearUpgrades' in old_research and 'UpgradeLevels' in old_research['LinearUpgrades']:
                    #     old_levels = old_research['LinearUpgrades']['UpgradeLevels']
                    #     new_levels = {
                    #         "LRUChunkLimitAdd": old_levels.get("LRUChunkLimitAdd", 0),
                    #         "LRUDummy_Zero": 0,
                    #         "LRUGlobalSpeed": max([old_levels.get("LRUBeltSpeed", 0), old_levels.get("LRUCuttingSpeed", 0), old_levels.get("LRUStackingSpeed", 0), old_levels.get("LRUPaintingSpeed", 0)] + [0]),
                    #         "LRUHubInputSize": old_levels.get("LRUHubInputSize", 0),
                    #         "LRUShapeQuantity": old_levels.get("LRUShapeQuantity", 0),
                    #         "LRUTrainCapacity": old_levels.get("LRUTrainCapacity", 0),
                    #         "LRUTrainSpeed": old_levels.get("LRUTrainSpeed", 0)
                    #     }
                    #     template_research.setdefault('LinearUpgrades', {})['UpgradeLevels'] = new_levels
                        
                    if 'Shapes' in old_research and 'StoredShapes' in old_research['Shapes']:
                        template_research.setdefault('Shapes', {})['StoredShapes'] = old_research['Shapes']['StoredShapes']
                        
                    if 'PlayerLevelGoals' in old_research and 'GoalLevels' in old_research['PlayerLevelGoals']:
                        old_goals = old_research['PlayerLevelGoals']['GoalLevels']
                        new_goals = {}
                        template_goals = template_research.get("PlayerLevelGoals", {}).get("GoalLevels", {})
                        for key in template_goals.keys():
                            new_goals[key] = old_goals.get(key, template_goals[key])
                        
                        # Special mappings for version/key compatibility
                        if "Random2" in old_goals:
                            new_goals["Random2_Crystals"] = old_goals["Random2"]
                        if "Reuse_TrainHubDelivery" in old_goals:
                            new_goals["Reuse_Vortex"] = old_goals["Reuse_TrainHubDelivery"]
                        template_research.setdefault('PlayerLevelGoals', {})['GoalLevels'] = new_goals
                    
                    # 4. WRITE OUT THE ZIP
                    for item in zin_template.infolist():
                        if item.filename == "savegame.json":
                            zout.writestr(item.filename, json.dumps(template_savegame).encode('utf-8'))
                        elif item.filename == "research.json":
                            zout.writestr(item.filename, json.dumps(template_research).encode('utf-8'))
                        elif item.filename == "local-player.json":
                            zout.writestr(item.filename, json.dumps(template_player).encode('utf-8'))
                        else:
                            # Exact byte-for-byte copy, this avoids corrupting maps/main/meta/ since Python zip library accurately pulls 256 bytes from template
                            zout.writestr(item, zin_template.read(item.filename))

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    memory_file.seek(0)
    
    return send_file(
        memory_file,
        as_attachment=True,
        download_name='upgraded_ngp_save.spz2',
        mimetype='application/zip'
    )

if __name__ == '__main__':
    app.run(debug=True, port=6004)
