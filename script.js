document.addEventListener('DOMContentLoaded', () => {
    const fileStructure = {
        'README.md': 'file',
        'Dockerfile': 'file',
        'docker-compose.yml': 'file',
        'backend': {
            'Dockerfile': 'file',
            '.env.template': 'file',
            'requirements.txt': 'file',
            'alembic.ini': 'file',
            'alembic': {
                'README': 'file',
                'env.py': 'file',
                'script.py.mako': 'file',
                'versions': {
                    'c1a7c5b6e4d5_initial_migration.py': 'file',
                    'a1b2c3d4e5f6_add_player_value_and_source_mapping_tables.py': 'file'
                }
            },
            'app': {
                '__init__.py': 'file',
                'main.py': 'file',
                'config.py': 'file',
                'api': {
                    '__init__.py': 'file',
                    'routers': {
                        '__init__.py': 'file',
                        'waiver_router.py': 'file'
                    },
                    'v1': {
                        '__init__.py': 'file',
                        'endpoints': {
                            '__init__.py': 'file',
                            'fantasy.py': 'file',
                            'yahoo.py': 'file',
                            'trade_router.py': 'file'
                        }
                    }
                },
                'db': {
                    '__init__.py': 'file',
                    'base_class.py': 'file',
                    'session.py': 'file'
                },
                'models': {
                    '__init__.py': 'file',
                    'user.py': 'file',
                    'league.py': 'file',
                    'team.py': 'file',
                    'player.py': 'file'
                },
                'schemas': {
                    'trade.py': 'file',
                    'waiver.py': 'file'
                },
                'services': {
                    '__init__.py': 'file',
                    'player_data_service.py': 'file',
                    'trade_analyzer_service.py': 'file',
                    'yahoo_api.py': 'file',
                    'waiver_service.py': 'file'
                },
                'scripts': {
                    '__init__.py': 'file',
                    'seed_player_data.py': 'file'
                }
            }
        },
        'frontend': {
            'package.json': 'file',
            'vite.config.js': 'file',
            'index.html': 'file',
            'src': {
                'main.jsx': 'file',
                'App.jsx': 'file',
                'index.css': 'file',
                'components': {
                    '.gitkeep': 'file'
                },
                'pages': {
                    'HomePage.jsx': 'file',
                    'LeaguePage.jsx': 'file',
                    'WaiverWirePage.jsx': 'file',
                    'TradeAnalyzerPage.jsx': 'file'
                },
                'services': {
                    'api.js': 'file'
                }
            }
        }
    };

    const fileTreeContainer = document.getElementById('file-tree');
    const fileNameElement = document.getElementById('file-name');
    const fileContentElement = document.getElementById('file-content');
    const projectSummaryElement = document.getElementById('project-summary');
    const fileContentWrapper = document.getElementById('file-content-wrapper');
    const projectOverviewBtn = document.getElementById('project-overview-btn');

    function showProjectSummary() {
        projectSummaryElement.classList.remove('hidden');
        fileContentWrapper.classList.add('hidden');
        fileNameElement.innerHTML = `<i data-lucide="book-open" class="w-5 h-5 mr-2 text-gray-400"></i> <span>Project Overview</span>`;
        lucide.createIcons();
        document.querySelectorAll('.file-item.active').forEach(el => el.classList.remove('active'));
    }

    projectOverviewBtn.addEventListener('click', showProjectSummary);

    function createTree(data, path = '') {
        const ul = document.createElement('ul');
        if (path !== '') ul.classList.add('hidden');

        const sortedKeys = Object.keys(data).sort((a, b) => {
            const aIsFile = typeof data[a] === 'string';
            const bIsFile = typeof data[b] === 'string';
            if (aIsFile === bIsFile) {
                return a.localeCompare(b);
            }
            return aIsFile ? 1 : -1;
        });

        for (const key of sortedKeys) {
            const li = document.createElement('li');
            const currentPath = path ? `${path}/${key}` : key;
            const item = data[key];

            if (typeof item === 'object') {
                const folderDiv = document.createElement('div');
                folderDiv.className = 'folder-item';
                folderDiv.innerHTML = `<i data-lucide="folder" class="w-4 h-4 mr-2 text-yellow-500"></i><span>${key}</span>`;
                folderDiv.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const subUl = li.querySelector('ul');
                    if (subUl) {
                        subUl.classList.toggle('hidden');
                        const icon = folderDiv.querySelector('i');
                        icon.setAttribute('data-lucide', subUl.classList.contains('hidden') ? 'folder' : 'folder-open');
                        lucide.createIcons();
                    }
                });
                li.appendChild(folderDiv);
                li.appendChild(createTree(item, currentPath));
            } else {
                const fileDiv = document.createElement('div');
                fileDiv.className = 'file-item';
                fileDiv.innerHTML = `<i data-lucide="file-text" class="w-4 h-4 mr-2 text-blue-400"></i><span>${key}</span>`;
                fileDiv.dataset.path = currentPath;
                fileDiv.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    projectSummaryElement.classList.add('hidden');
                    fileContentWrapper.classList.remove('hidden');

                    const filePath = e.currentTarget.dataset.path;
                    
                    document.querySelectorAll('.file-item.active').forEach(el => el.classList.remove('active'));
                    e.currentTarget.classList.add('active');
                    
                    fileNameElement.innerHTML = `<i data-lucide="file-code-2" class="w-5 h-5 mr-2 text-gray-400"></i> <span>${filePath}</span>`;
                    lucide.createIcons();
                    fileContentElement.textContent = 'Loading...';

                    try {
                        let fetchPath = filePath;
                        if (filePath.endsWith('.py')) {
                            fetchPath = filePath.substring(0, filePath.length - 3) + '_py';
                        }
                        const response = await fetch(fetchPath);
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        const text = await response.text();
                        fileContentElement.textContent = text;
                    } catch (error) {
                        console.error('Error loading file:', error);
                        fileContentElement.textContent = `Error loading file: ${filePath}.\nContent may not be available in this interactive viewer.`;
                    }
                });
                li.appendChild(fileDiv);
            }
            ul.appendChild(li);
        }
        return ul;
    }

    fileTreeContainer.appendChild(createTree(fileStructure));
    lucide.createIcons();
    
    showProjectSummary();
});
